from JumpScale import j


class Actions(ActionsBaseMgmt):

    def install(self, service):
        nodes = service.getProducers('os')
        cluster = {'shard': [], 'config': [], 'mongos': []}
        number_of_shards = 1
        clusterconfig = service.hrd.get('clusterconfig')
        for node in nodes:
            executor = node.executor
            nodeconfig = clusterconfig.get(node.instance, '')
            nodeconfig = j.data.tags.getObject(nodeconfig)
            nodeconfig = nodeconfig.getDict()
            for role, port in nodeconfig.items():
                if role not in nodeconfig:
                    continue
                roleconfig = {'executor': executor}
                roleconfig['addr'] = node.instance
                roleconfig['private_port'] = int(port)
                roleconfig['public_port'] = int(port)
                # TODO (*2*) path to db should be mounted
                roleconfig['dbdir'] = '/var/mongodbs/%s' % role
                cluster.get(role, []).append(roleconfig)
                if role == 'shard':
                    number_of_shards += 1

        cuisine = j.tools.cuisine.get()
        cuisine.apps.mongodb.mongoCluster(cluster['shard'], cluster['config'], cluster['mongos'], shards_replica_set_counts=number_of_shards)
        self.start(service=service)

    def start(self, service):
        nodes = service.getProducers('os')
        cluster = {'shard': 'ourmongod', 'config': 'ourmongod_cfg', 'mongos': 'ourmongos'}
        clusterconfig = service.hrd.get('clusterconfig')
        for node in nodes:
            executor = node.executor
            nodeconfig = clusterconfig.get(node.instance, '')
            nodeconfig = j.data.tags.getObject(nodeconfig)
            nodeconfig = nodeconfig.getDict()
            for role in nodeconfig:
                if role not in nodeconfig:
                    continue
                executor.cuisine.processmanager.start(cluster[role])
