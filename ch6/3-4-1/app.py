from langchain.agents import initialize_agent, Tool
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain.prompts import PromptTemplate
from langchain.agents import AgentType
from langchain_openai import ChatOpenAI

def create_prompt(user_input):
    prompt = PromptTemplate(
        input_variables=["theme"], 
        template="""
        당신은 뉴스 기사를 쓰는 영어권 블로거입니다.
        다음 주제에 대해 영어 구글 검색을 통해 최신 정보를 얻고, 검색된 정보를 바탕으로 리스트를 작성해 한국어로 출력해 주세요. 목록에는 서비스 이름과 공식 URL, 서비스 개요를 포함시켜 주세요.
        ###
        테마: {theme}
        """
    )
    return prompt.format(theme=user_input)

def define_tools():
    search = GoogleSearchAPIWrapper()
    return [
        Tool(
            name = "Search",
            func=search.run,
            description="useful for when you need to answer questions about current events. You should ask targeted questions"
        ),
    ]

def write_response_to_file(response, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response)
    print('출력이 완료되었습니다')

def main():
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", max_tokens=2000)
    tools = define_tools()
    agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS)
    prompt = create_prompt(input("글의 테마를 입력해 주세요: "))
    response = agent.run(prompt)
    write_response_to_file(response, 'output.txt')

if __name__ == "__main__":
    main()
