MyList = [('one', [1,2,3,4,5,5]),('one', [1,2,3,4,5,5]), ('two', 2), ('three', 3)]
MyDict = dict(MyList)
print(MyDict)





# flag = dict_to_pickle()
        # if flag:
        #     with open('interface\old_conv.pkl', 'rb') as f:
        #         # Load the data from the file
        #         old_conv = pickle.load(f)
        #
        with open("interface/old_conv.pkl", "rb") as f:
            old_conv = pickle.load(f)

        print(f"old conversation: {old_conv}")