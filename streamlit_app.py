import streamlit as st
from PIL import Image

# Set page config
st.set_page_config(
    page_title="Emmaculate Cleaning Service - Premium Cleaning in Jamaica",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for branding
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
    /* Global Styles */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        color: #1B2E4B;
        background-color: #F8F9FA;
    }

    h1, h2, h3, .serif-font {
        font-family: 'Playfair Display', serif !important;
        font-weight: 700;
        color: #1B2E4B;
    }

    /* Buttons */
    .stButton > button {
        background-color: #F5820A !important;
        color: white !important;
        border-radius: 5px !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #1B2E4B !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    /* WhatsApp Floating Button */
    .whatsapp-float {
        position: fixed;
        width: 60px;
        height: 60px;
        bottom: 40px;
        right: 40px;
        background-color: #25d366;
        color: #FFF;
        border-radius: 50px;
        text-align: center;
        font-size: 30px;
        box-shadow: 2px 2px 3px #999;
        z-index: 100;
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
    }

    /* Custom Cards */
    .service-card {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-bottom: 4px solid #7DC921;
        height: 100%;
        transition: transform 0.3s ease;
    }
    .service-card:hover {
        transform: translateY(-5px);
    }

    /* Hero Section */
    .hero-container {
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #1B2E4B 0%, #2c4a7a 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 3rem;
        text-align: center;
    }
    .hero-container h1 {
        color: white !important;
        font-size: 3.5rem;
        margin-bottom: 1.5rem;
    }

    /* Process Steps */
    .step-circle {
        background: #7DC921;
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-bottom: 1rem;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    </style>

    <!-- WhatsApp Floating Button -->
    <a href="https://wa.me/18760000000" class="whatsapp-float" target="_blank">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="35px" />
    </a>
""", unsafe_allow_html=True)

# Main layout logic starts here
def main():
    # Header / Navigation
    col_logo, col_nav = st.columns([1, 2])
    with col_logo:
        st.image("logo.png", width=150)

    with col_nav:
        st.markdown("<br>", unsafe_allow_html=True)
        # Placeholder for navigation if needed, or just align right
        pass

    # Step 2: Hero Section
    st.markdown("""
        <div class="hero-container">
            <h1>Experience Immaculate Standards.</h1>
            <p style="font-size: 1.2rem; opacity: 0.9; max-width: 700px; margin: 0 auto 2rem;">
                Jamaica's premium cleaning service for those who demand excellence.
                From luxury residences to high-traffic commercial spaces.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_btn_hero, _ = st.columns([1, 3])
    with col_btn_hero:
        if st.button("Get a Free Quote", key="hero_cta"):
            st.toast("Redirecting to booking form...")

    st.markdown("---")

    # Step 3: Services Grid
    st.markdown("<h2 style='text-align: center;'>Our Specialized Services</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    services = [
        {"title": "Residential", "desc": "Deep cleaning for your sanctuary.", "icon": "🏠"},
        {"title": "Commercial", "desc": "Professional upkeep for businesses.", "icon": "🏢"},
        {"title": "Post-Construction", "desc": "Making your new space move-in ready.", "icon": "🏗️"},
        {"title": "Upholstery", "desc": "Revitalizing your furniture and fabrics.", "icon": "🛋️"},
        {"title": "Mold Treatment", "desc": "Specialized removal and prevention.", "icon": "🧪"}
    ]

    cols = st.columns(3)
    for i, service in enumerate(services):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="service-card">
                    <h3>{service['icon']} {service['title']}</h3>
                    <p>{service['desc']}</p>
                </div>
                <br>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Step 4: Before & After Gallery
    st.markdown("<h2 style='text-align: center;'>The Emmaculate Difference</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Real results from our recent projects.</p>", unsafe_allow_html=True)

    col_ba1, col_ba2 = st.columns(2)
    with col_ba1:
        st.image("https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&q=80&w=800", caption="Before")
    with col_ba2:
        st.image("https://images.unsplash.com/photo-1527515637462-cff94eecc1ac?auto=format&fit=crop&q=80&w=800", caption="After")

    st.markdown("---")

    # Step 5: 4-Step Process
    st.markdown("<h2 style='text-align: center;'>Our Simple Process</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    p_cols = st.columns(4)
    steps = [
        ("Inquiry", "Reach out via web or WhatsApp."),
        ("Assessment", "We evaluate your specific needs."),
        ("Quote", "Receive a transparent, flat-rate quote."),
        ("Service", "Our professionals transform your space.")
    ]

    for i, (title, desc) in enumerate(steps):
        with p_cols[i]:
            st.markdown(f"""
                <div style="text-align: center;">
                    <div class="step-circle" style="margin: 0 auto 1rem;">{i+1}</div>
                    <h4>{title}</h4>
                    <p style="font-size: 0.9rem;">{desc}</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Step 6: Testimonials
    st.markdown("<h2 style='text-align: center;'>What Our Clients Say</h2>", unsafe_allow_html=True)
    t_cols = st.columns(2)
    with t_cols[0]:
        st.info("“The attention to detail is unmatched. My home has never felt this clean!” - *Sarah R., Kingston*")
    with t_cols[1]:
        st.info("“Reliable and professional. They handled our office move-out cleaning perfectly.” - *James W., Tech Hub JA*")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-weight: 600; opacity: 0.7;'>TRUSTED BY JAMAICA'S FINEST</p>", unsafe_allow_html=True)
    logo_strip_cols = st.columns(5)
    for i in range(5):
        with logo_strip_cols[i]:
            st.markdown(f"<div style='text-align: center; filter: grayscale(100%); opacity: 0.5;'>[COMPANY {i+1}]</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Step 7: Booking Form
    st.markdown("<h2 style='text-align: center;'>Book Your Service</h2>", unsafe_allow_html=True)
    with st.form("booking_form"):
        col_f1, col_f2 = st.columns(2)
        name = col_f1.text_input("Full Name")
        email = col_f2.text_input("Email Address")
        service_type = st.selectbox("Service Required", ["Residential", "Commercial", "Post-Construction", "Upholstery", "Mold Treatment"])
        message = st.text_area("Details (Special requests, square footage, etc.)")

        submitted = st.form_submit_button("Send Inquiry")
        if submitted:
            # Construct WhatsApp message
            wa_msg = f"New Inquiry from {name}%0AEmail: {email}%0AService: {service_type}%0ADetails: {message}"
            wa_link = f"https://wa.me/18760000000?text={wa_msg}"

            st.success("Thank you! Your inquiry has been prepared.")
            st.markdown(f"""
                <a href="{wa_link}" target="_blank" style="text-decoration:none;">
                    <div style="background-color:#25d366; color:white; padding:0.5rem 1rem; border-radius:5px; text-align:center; font-weight:bold;">
                        Finish Booking on WhatsApp
                    </div>
                </a>
                <p style="font-size:0.8rem; text-align:center; margin-top:0.5rem;">Or check your email for a confirmation (Simulation).</p>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Step 8: Footer
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    with footer_col1:
        st.image("logo.png", width=100)
        st.write("Emmaculate Cleaning Service")
        st.write("Jamaica's Choice for Premium Cleaning.")

    with footer_col2:
        st.markdown("#### Contact Us")
        st.write("📞 +1 (876) 000-0000")
        st.write("📧 info@emmaculateja.com")
        st.write("📍 Kingston, Jamaica")

    with footer_col3:
        st.markdown("#### Follow Us")
        st.write("Instagram | Facebook | LinkedIn")

    st.markdown("<br><p style='text-align: center; opacity: 0.5; font-size: 0.8rem;'>© 2023 Emmaculate Cleaning Service. Built with Pure Tropics in mind.</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
