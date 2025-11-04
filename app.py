import streamlit as st
import requests

# 페이지 기본 설정
st.set_page_config(page_title="🏛️ The Met Museum API", layout="wide")
st.title("🏛️ The Met Museum Open API Viewer")

st.write("🔍 아래 검색창에 작가명이나 주제를 입력하면, The Met Museum 컬렉션에서 작품을 불러옵니다.")

# 검색창
query = st.text_input("검색어 (예: van gogh, korea, ceramic 등)", value="van gogh")

# 검색 버튼
if st.button("검색"):
    if not query.strip():
        st.warning("검색어를 입력해주세요.")
    else:
        try:
            # 1️⃣ 작품 검색
            search_url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
            params = {"q": query, "hasImages": "true"}
            res = requests.get(search_url, params=params)
            res.raise_for_status()
            data = res.json()

            total = data.get("total", 0)
            st.write(f"총 {total}개의 결과 중 일부만 표시합니다.")

            object_ids = (data.get("objectIDs") or [])[:9]

            if not object_ids:
                st.info("검색 결과가 없습니다. 다른 키워드를 시도해보세요.")
            else:
                cols = st.columns(3)
                for i, obj_id in enumerate(object_ids):
                    # 2️⃣ 작품 상세정보 가져오기
                    detail_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}"
                    detail_res = requests.get(detail_url)
                    detail_data = detail_res.json()

                    title = detail_data.get("title", "Untitled")
                    artist = detail_data.get("artistDisplayName", "Unknown")
                    img_url = detail_data.get("primaryImageSmall", "")
                    date = detail_data.get("objectDate", "")
                    dept = detail_data.get("department", "")

                    # 3️⃣ 결과 표시
                    with cols[i % 3]:
                        if img_url:
                            st.image(img_url, caption=f"{title} ({artist})", use_container_width=True)
                        st.write(f"**작가:** {artist}")
                        st.write(f"**제작연도:** {date}")
                        st.write(f"**부서:** {dept}")

        except requests.RequestException as e:
            st.error(f"API 요청 중 오류 발생: {e}")
