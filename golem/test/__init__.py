import inelegant.finder

load_tests = inelegant.finder.TestFinder('golem.test.animator').load_tests

if __name__ == '__main__':
    unittest.main()


