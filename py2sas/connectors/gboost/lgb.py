from .core import TreeParser


class LightgbmParser(TreeParser):
    def __init__(self, booster):
        super(LightgbmParser, self).__init__()

        self.booster = booster
        
        self.dump = booster.dump_model()
        if self.dump['objective'] != 'binary sigmoid:1':
            raise Exception("Unfortunately only binary sigmoig objective function is supported right now. Your objective is %s. Please, open an issue at https://gitlab.sas.com/from-russia-with-love/lgb2sas." % dump['objective'])

        self.features = self.dump['feature_names']
        self.out_transform = "1 / (1 + exp(-{0}))"


    def _not_leaf(self, node):
        return 'split_feature' in node


    def _get_var(self, node):
        return self.features[node[self.split_name]]


    def _go_left(self, node):
        return node['default_left']

    
    def _go_right(self, node):
        return (not node['default_left'])


    def _left_node(self, node):
        return node['left_child']

    
    def _right_node(self, node):
        return node['right_child']


    def _missing_node(self, node):
        return None

    
    def _split_value(self, node):
        return node['threshold']


    def _decision_type(self, node):
        return node['decision_type']


    def _leaf_value(self, node):
        return node['leaf_value']

    
    def iter_trees(self):
        for tree in self.dump['tree_info']:
            yield tree['tree_index'], tree['tree_structure']
