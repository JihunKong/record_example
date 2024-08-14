import streamlit as st
import openai

# OpenAI API 키 설정
openai.api_key = st.secrets["openai_api_key"]

def generate_sespec(prompt):
    response = openai.chat.Completion.create(
        engine="gpt-4o-mini",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def main():
    st.title("세부능력 및 특기사항(세특) 작성 도우미")

    # 1. 사용자 정보 수집
    st.header("1. 사용자 정보 수집")
    
    희망_진로 = st.text_input("희망하는 진로, 직업, 학과 또는 전공 분야를 알려주세요.", 
                          help="예: 한국어 교사, 심리학자, 기계공학, 경영학, TV 방송국 PD 등")
    
    교과_단원명 = st.text_input("세특을 작성할 교과 또는 단원명을 알려주세요.", 
                           help="예: 화학반응, 생물유전, 윤리와 사상, 미디어 리터러시, 삼각함수, 조선시대 등")
    
    활동_내용 = st.text_area("수행한 활동을 입력해주세요.", 
                         help="예: '[코스모스 - 칼 세이건] 독서', '이중슬릿 실험', '러시아-우크라이나 전쟁이 미중 패권 구조에 미치는 영향 연구', '노인 빈곤율 주제 발표' 등")

    if st.button("세특 초안 생성"):
        # 2. 세특 초안 작성
        prompt = f"""
        학생의 희망 진로: {희망_진로}
        교과/단원명: {교과_단원명}
        수행한 활동: {활동_내용}

        위 정보를 바탕으로 다음과 같은 구조로 세부능력 및 특기사항(세특)의 초안을 작성해주세요:

        1. {교과_단원명} 관련 교과서 내용 학습 및 호기심 유발
        2. 수행한 활동에 대한 설명 (역할, 과정, 결과)
        3. 새롭게 알게 된 점, 소감, 아쉬운 점
        4. 향후 학습 계획 또는 발전 방향

        세특은 구체적이고 생생하게 작성하되, 학생의 성장과 발전을 강조해주세요.
        """

        with st.spinner('세특 초안을 생성 중입니다...'):
            초안 = generate_sespec(prompt)

        st.subheader("2. 세특 초안")
        st.write(초안)

        # 3. 세특 상세화
        st.subheader("3. 세특 상세화")
        상세화_옵션 = st.multiselect(
            "세특에 추가로 포함할 내용을 선택하세요:",
            ["실험/탐구 활동 상세 설명", "도전 과제 및 극복 과정", "교과서 내용과의 연계"]
        )

        if st.button("세특 상세화"):
            상세화_prompt = f"""
            다음 세특 초안을 바탕으로, 선택된 옵션에 대해 더욱 상세한 내용을 추가해주세요:

            {초안}

            추가할 내용:
            {', '.join(상세화_옵션)}

            각 옵션에 대해 2-3문장 정도의 구체적인 설명을 추가해주세요.
            """

            with st.spinner('세특을 상세화하고 있습니다...'):
                상세_세특 = generate_sespec(상세화_prompt)

            st.write(상세_세특)

            # 4. 세특 최종 정리
            st.subheader("4. 세특 최종 정리")
            if st.button("최종 세특 생성"):
                최종_정리_prompt = f"""
                다음의 상세 세특을 바탕으로 최종 세특을 작성해주세요:

                {상세_세특}

                최종 세특은 다음 구조를 따라야 합니다:
                1. {교과_단원명} 관련 내용 (500자 이내로 요약)
                2. 학생의 역량 평가 (성장 과정 및 역량 평가)
                3. 종합적 검토 (교사의 종합적인 의견)

                전체 길이는 1000자를 넘지 않도록 해주세요.
                """

                with st.spinner('최종 세특을 생성 중입니다...'):
                    최종_세특 = generate_sespec(최종_정리_prompt)

                st.write(최종_세특)

                # 글자 수 확인
                st.info(f"최종 세특 글자 수: {len(최종_세특)}")

if __name__ == "__main__":
    main()
