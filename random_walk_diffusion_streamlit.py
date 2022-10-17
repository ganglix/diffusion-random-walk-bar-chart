import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(layout="wide")
# front end main page
header = st.beta_container()
with header:
    st.title("Diffusion - random movement of atoms")
    st.text(
        "This app uses a bar chart to visualize the diffusion process due to the random movement of atoms in 1-D."
    )

# data input from user
st.sidebar.header("Parameter settings")

# sidebar parameter setting
no_move_prob = st.sidebar.number_input(
    "Probability of atom staying in place", 
    value=0.8, step=0.01, min_value = 0.01, max_value=0.99, format="%.3f"
)
left_move_prob = (1-no_move_prob)/2  # ft/ns
right_move_prob = left_move_prob
st.sidebar.write(f"Therefore, left-move probability = right-move probability = {left_move_prob}.")

st.sidebar.write("number of atoms")
grid_0 = st.sidebar.number_input(
    "grid 0", value=int(1e5), step=1000, min_value = int(1e3), max_value=int(1e6)
)
grid_1 = st.sidebar.number_input(
    "grid 1", value=int(1e5), step=1000, min_value = int(1e3), max_value=int(1e6)
)
grid_2 = st.sidebar.number_input(
    "grid 2", value=int(1e5), step=1000, min_value = int(1e3), max_value=int(1e6)
)
grid_3 = st.sidebar.number_input(
    "grid 3", value=int(1e5), step=1000, min_value = int(1e3), max_value=int(1e6)
)
grid_4 = st.sidebar.number_input(
    "grid 4", value=int(1e5), step=1000, min_value = int(1e3), max_value=int(1e6)
)
grid_5 = st.sidebar.number_input(
    "grid 5", value=int(1e4), step=1000, min_value = int(1e3), max_value=int(1e6)
)
grid_6 = st.sidebar.number_input(
    "grid 6", value=int(1e4), step=1000, min_value = int(1e3), max_value=int(1e6)
)
grid_7 = st.sidebar.number_input(
    "grid 7", value=int(1e4), step=1000, min_value = int(1e3), max_value=int(1e6)
)
grid_8 = st.sidebar.number_input(
    "grid 8", value=int(1e4), step=1000, min_value = int(1e3), max_value=int(1e6)
)
grid_9 = st.sidebar.number_input(
    "grid 9", value=int(1e4), step=1000, min_value = int(1e3), max_value=int(1e6)
)

c_init = np.array([grid_0, grid_1, grid_2, grid_3, grid_4, grid_5, grid_6, grid_7, grid_8, grid_9])


def choose_left_right(number, p_no_move=no_move_prob, p_left=left_move_prob, p_right=right_move_prob):
    """label atoms with 0, -1, 1, meaning no move, move left, move right"""
    label = np.random.choice([0, -1, 1], number, p=[p_no_move,p_left,p_right])
    left_no = len(label[label == -1])
    right_no = len(label[label == 1])
    return (left_no, right_no)

@st.cache
def c_time_steps(n, c_init=c_init):
    c = c_init
    c_lis = []
    c_lis.append(c)
    
    # step
    if n == 0:
        None
    else:
        for i in range(n):
            left_lis = []
            right_lis = []
            for v in c:
                left_no, right_no = choose_left_right(v)
                left_lis.append(left_no)
                right_lis.append(right_no)
            # update c
            # no move
            c = c - np.array(left_lis) - np.array(right_lis)
            # add left move
            c[0:-1] = c[0:-1] + np.array(left_lis)[1:]
            c[0] = c[0] + np.array(left_lis)[0]
            # add right move
            c[1:] = c[1:] + np.array(right_lis)[0:-1]
            c[-1] = c[-1] + np.array(right_lis)[-1]
            c_lis.append(c)
    return c_lis



st.header("Parameter summary")
st.write(f"atom count {c_init}")
st.write("Atom movement probability")
st.write(f"stay in place: {no_move_prob}, move left: {left_move_prob}, move right: {right_move_prob}")

st.header("First, select the total time steps to simulate")
total_time_step = st.number_input(
    "total time step", value=20, step=1, min_value = 1, max_value=1000,
)
st.spinner(text="In progress...")

# compute for n steps
n=total_time_step

# if st.checkbox("check to compute"):
c_lis = c_time_steps(n)
# x_grid = list(range(len(c_lis[0])))
st.header("Now use the slider to visualize atom count at different time steps in a bar chart")

# if st.button("plot"):
step = st.slider("time step", value=0, max_value=n)
st.bar_chart(data = c_lis[step])

