import streamlit as st
from database import get_donations, update_donation_status


def ngo_dashboard():

    st.title("🏢 NGO Dashboard")
    st.write("View and manage available food donations.")

    donations = get_donations()

    if donations:

        for donation in donations:

            st.divider()

            st.subheader(donation[2])

            st.write("Donor:", donation[1])
            st.write("Quantity:", donation[3], "portions")
            st.write("Food Category:", donation[4])
            st.write("Pickup Location:", donation[7])
            st.write("Collection Deadline:", donation[6])
            st.write("Status:", donation[9])

            if donation[9] == "Pending":

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        "Accept Donation",
                        key=f"accept_{donation[0]}"
                    ):
                        update_donation_status(
                            donation[0], "Accepted"
                        )
                        st.success("Donation Accepted!")
                        st.rerun()

                with col2:
                    if st.button(
                        "Decline Donation",
                        key=f"decline_{donation[0]}"
                    ):
                        update_donation_status(
                            donation[0], "Declined"
                        )
                        st.warning("Donation Declined!")
                        st.rerun()

            else:
                
                st.markdown("""
<div style="
    background-color: #fff3cd;
    color: #14532d;
    padding: 15px;
    border: 2px solid #176b45;
    border-radius: 10px;
    font-size: 17px;
    font-weight: bold;
">
    This donation has already been processed.
</div>
""", unsafe_allow_html=True)

    else:
        st.info("No food donations available.")