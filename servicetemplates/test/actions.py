from JumpScale import j


class Actions(ActionsBaseMgmt):
    def install(self, service):
        use_node = None
        clusterconfig = service.parent.hrd.get('clusterconfig')
        for node, nodedata in clusterconfig.items():
            nodeconfig = j.data.tags.getObject(nodedata)
            nodeconfig = nodeconfig.getDict()
            if nodeconfig.get('mongos', None):
                candidates = service.parent.producers.get('os')
                use_node = [candidate for candidate in candidates if candidate.instance == node][0]
                break

        cl = j.clients.mongodb.get(use_node.hrd.get('ssh.addr'), port=27019)
        db = cl.get_database('test0')
        for i in range(1000):
            db.test.insert_one({'title': 'test_%s' % i})
