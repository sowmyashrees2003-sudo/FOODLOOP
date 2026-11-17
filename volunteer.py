import streamlit as st
import cv2
import numpy as np

from database import get_donations, update_donation_status
from qr_system import generate_qr_code


def read_qr_code(image):

    image_bytes = np.asarray(
        bytearray(image.getvalue()),
        dtype=np.uint8
    )

    decoded_image = cv2.imdecode(
        image_bytes,
        cv2.IMREAD_COLOR
    )

    detector = cv2.QRCodeDetector()

    data, points, _ = detector.detectAndDecode(
        decoded_image
    )

    return data


def volunteer_dashboard():

    st.title("🚚 Volunteer Dashboard")

    st.write(
        "View accepted food donations, "
        "verify pickups and manage collections."
    )

    donations = get_donations()
    

    # QR CODE SCANNER

    st.divider()
    st.subheader("📷 Scan Donation QR Code")

    uploaded_qr = st.file_uploader(
        "Upload a photo of the donation QR code",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_qr is not None:

        scanned_data = read_qr_code(uploaded_qr)

        if scanned_data:

            st.success("QR Code detected!")
            st.write("QR Data:", scanned_data)

            try:

                donation_id = int(
                    scanned_data.replace(
                        "FOODLOOP-DONATION-", ""
                    )
                )

                matching_donation = next(
                    (
                        d for d in donations
                        if d[0] == donation_id
                    ),
                    None
                )
                

                if matching_donation is None:

                    st.error("Donation ID not found!")

                elif matching_donation[9] == "Collected":

                    st.success(
                        "This donation has already been collected!"
                    )

                elif str(matching_donation[9]).strip().lower() == "collected":

                    st.success(
                        "This donation has already been collected successfully!"
                    )

                elif str(matching_donation[9]).strip().lower() != "accepted":

                    st.warning(
                        "Donation is not available for collection."
                    )

                else:

                    st.success(
                        f"Verified: {matching_donation[2]}"
                    )

                    st.write(
                        "Pickup Location:",
                        matching_donation[7]
                    )

                    if st.button(
                        "Confirm QR Handover",
                        key=f"verify_{donation_id}"
                    ):

                        update_donation_status(
                            donation_id,
                            "Collected"
                        )

                        st.success(
                            "Handover verified successfully!"
                        )

                        st.rerun()

            except ValueError:

                st.error("Invalid FOODLOOP QR code.")

        else:

            st.error(
                "Could not read QR code. Try another image."
            )

    # VOLUNTEER PICKUP DASHBOARD

    st.divider()
    st.subheader("📦 Available Donations for Pickup")

    donations = get_donations()

    accepted_donations = [
        donation for donation in donations
        if donation[9] == "Accepted"
    ]

    if accepted_donations:

        st.success(
            f"{len(accepted_donations)} donations available for pickup."
        )

        for donation in accepted_donations:

            st.divider()

            st.subheader(f"🍱 {donation[2]}")

            st.write("Donation ID:", donation[0])
            st.write("Donor:", donation[1])
            st.write("Quantity:", donation[3], "portions")
            st.write("Food Category:", donation[4])
            st.write("Pickup Location:", donation[7])
            st.write("Collection Deadline:", donation[6])
            st.write("Status:", donation[9])

            st.subheader("📱 Donation QR Code")

            qr_image = generate_qr_code(donation[0])

            st.image(
                qr_image,
                caption=f"Donation ID: {donation[0]}",
                width=200
            )

            if st.button(
                "Mark as Collected",
                key=f"collected_{donation[0]}"
            ):

                update_donation_status(
                    donation[0],
                    "Collected"
                )

                st.success(
                    "Donation marked as Collected!"
                )

                st.rerun()

    else:
         st.markdown("""
<div style="
    background-color: #dbeafe;
    color: #1e3a8a;
    padding: 15px;
    border: 2px solid #2563eb;
    border-radius: 10px;
    font-size: 17px;
    font-weight: bold;
">
    No donations available for pickup.
</div>
""", unsafe_allow_html=True)  # COLLECTED DONATIONS HISTORY

    st.divider()
    st.subheader("✅ Collected Donations")

    donations = get_donations()

    collected_donations = [
        donation for donation in donations
        if str(donation[9]).strip().lower() == "collected"
    ]

    if collected_donations:

        for donation in collected_donations:

            st.divider()

            st.subheader(f"🍱 {donation[2]}")

            st.write("Donation ID:", donation[0])
            st.write("Donor:", donation[1])
            st.write("Quantity:", donation[3], "portions")
            st.write("Pickup Location:", donation[7])
            st.write("Status: Collected")

            qr_image = generate_qr_code(donation[0])

            st.image(
                qr_image,
                caption=f"Collected Donation QR - ID {donation[0]}",
                width=180
            )

    else:
        st.info("No collected donations yet.")
