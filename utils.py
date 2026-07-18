import streamlit as st


def section_header(title, subtitle):
    st.markdown(f"## {title}")
    st.caption(subtitle)
    st.divider()


def io_box(label_left, label_right, left_val, right_val):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**{label_left}**")
        st.code(left_val if left_val else " ", language=None)
    with c2:
        st.markdown(f"**{label_right}**")
        st.code(right_val if right_val else " ", language=None)