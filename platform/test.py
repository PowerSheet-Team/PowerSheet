from analysis import Analysis
from llm.impl import llm_cpu, llm_api

if __name__ == "__main__":
    analysis_test = Analysis(
        {'inputRange': 'Sheet1!A1:B5', 'outputRange': 'Sheet1!A6:B6', 'description': 'sum them up separately',
         'inputData': [[1, 11], [2, 22], [3, 33], [4, 44], [5, 55]], 'outputData': [['', '']]})

    llm = llm_api.LLM_API()
    context = llm.getContext()
    # print("result: ", context.query("Where are you from?"))
    query = analysis_test.gen_query()
    # response = context.query(query)
    # print(response)
    print(analysis_test.outputSection.width * analysis_test.outputSection.height)
    # print(analysis_test.apply_reply(response))
    print(analysis_test.apply_reply("<CELL>1111</CELL>  <CELL>2222</CELL>"))
    print(analysis_test.outputSection.data)
