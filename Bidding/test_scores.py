import scores as s
import unittest

#    @unittest.skip("skip for now")


class TestScores(unittest.TestCase):
    def test_1D_bid_and_made_by_W_All(self):
        entry = ['1D', 'W', '7']
        vulnerable = 'All'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 70])
 
    def test_1D_bid_plus_1_by_W_EW(self):
        entry = ['1D', 'W', '8']
        vulnerable = 'EW'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 90])
 
    def test_1DX_bid_plus_1_by_W_EW(self):
        entry = ['1DX', 'W', '8']
        vulnerable = 'EW'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 340])
     
    def test_1DX_bid_plus_2_by_E_None(self):
        entry = ['1DX', 'E', '9']
        vulnerable = 'None'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 340])
     
    def test_1DXX_bid_and_made_by_E_None(self):
        entry = ['1DXX', 'E', '7']
        vulnerable = 'None'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 230])
     
    def test_1H_bid_and_made_by_N_All(self):
        entry = ['1H', 'N', '7']
        vulnerable = 'All'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [80, 0])
 
    def test_1H_bid_plus_1_by_N_EW(self):
        entry = ['1H', 'N', '8']
        vulnerable = 'EW'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [110, 0])
 
    def test_1HX_bid_plus_1_by_S_EW(self):
        entry = ['1HX', 'S', '8']
        vulnerable = 'EW'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [260, 0])
     
    def test_1HX_bid_plus_2_by_S_None(self):
        entry = ['1HX', 'S', '9']
        vulnerable = 'None'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [360, 0])
    
    def test_1HXX_bid_plus_1_by_E_EW(self):
        entry = ['1HXX', 'E', '8']
        vulnerable = 'EW'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 1120])
    
    def test_1N_bid_plus_1_by_E_NS(self):
        entry = ['1N', 'E', '8']
        vulnerable = 'NS'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 120])
    
    def test_1N_bid_plus_1_by_E_All(self):
        entry = ['1N', 'E', '8']
        vulnerable = 'All'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 120])
    
    def test_2NX_bid_plus_1_by_E_All(self):
        entry = ['2NX', 'E', '9']
        vulnerable = 'All'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 890])
    
    def test_3N_bid_plus_1_by_N_None(self):
        entry = ['3N', 'N', '10']
        vulnerable = 'None'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [430, 0])

    def test_3NXX_bid_plus_1_by_N_NS(self):
        entry = ['3NXX', 'N', '10']
        vulnerable = 'NS'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [1400, 0])

    def test_6S_bid_plus_1_by_N_NS(self):
        entry = ['6S', 'N', '13']
        vulnerable = 'NS'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [1460, 0])

    def test_6S_bid_plus_1_by_W_None(self):
        entry = ['6S', 'W', '13']
        vulnerable = 'None'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 1010])

    def test_6SXX_bid_plus_1_by_E_None(self):
        entry = ['6SXX', 'E', '13']
        vulnerable = 'None'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 1820])

    def test_7SXX_bid_and_made_by_E_EW(self):
        entry = ['7SXX', 'E', '13']
        vulnerable = 'EW'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 2940])

    def test_7NXX_bid_and_made_by_E_EW(self):
        entry = ['7NXX', 'E', '13']
        vulnerable = 'EW'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 2980])
        
    def test_3S_down_2_by_S_EW(self):
        entry = ['3S', 'S', '7']
        vulnerable = 'EW'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 100])
        
    def test_3S_down_2_by_S_NS(self):
        entry = ['3S', 'S', '7']
        vulnerable = 'NS'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 200])

    def test_3SX_down_2_by_S_EW(self):
        entry = ['3SX', 'S', '7']
        vulnerable = 'EW'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 300])
        
    def test_3SX_down_2_by_S_NS(self):
        entry = ['3SX', 'S', '7']
        vulnerable = 'NS'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 500])
        
    def test_3SX_down_4_by_S_EW(self):
        entry = ['3SX', 'S', '5']
        vulnerable = 'EW'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 800])
        
    def test_3SX_down_4_by_S_NS(self):
        entry = ['3SX', 'S', '5']
        vulnerable = 'NS'
        result = s.getScores(entry, vulnerable)
        self.assertEqual(result, [0, 1100])
        

    