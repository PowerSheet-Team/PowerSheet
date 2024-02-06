from analysis import Analysis
from llm.impl import llm_cpu

if __name__ == "__main__":
    analysis_test = Analysis(
        {'inputRange': 'Sheet1!A1:B9', 'outputRange': 'Sheet1!C1:C9', 'description': '',
         'inputData': [['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', '']],
         'outputData': [[''], [''], [''], [''], [''], [''], [''], [''], ['']]
         }
    )

    LLM = llm_cpu.LLM()
    context = llm_cpu.Context()
    print("result: ", context.query("Where are you from?"))
