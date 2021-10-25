from optimus.tests.base import TestBase

class TestDFPandas(TestBase):
    def test_dataframe_dict_auto(self):
        data = {'object': [1, "2", 3.0], "int": [1, 2, 3], "float": [1.0, 2.0, 3.5]}
        df = self.op.create.dataframe(data)
        result = df.cols.data_type()
        expected = {'object': 'object', 'int': 'int64', 'float': 'float64'}

        self.assertTrue(results_equal(result, expected))