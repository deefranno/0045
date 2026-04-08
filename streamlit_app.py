import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Emmaculate Cleaning Service | Professional & Premium Cleaning",
    page_icon="🧼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS and Design System
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Playfair+Display:wght@700;900&display=swap');

    :root {
        --deep-navy: #1B2E4B;
        --vibrant-orange: #F5820A;
        --lime-green: #7DC921;
        --soft-white: #F8F9FA;
    }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: white;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: var(--deep-navy);
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sticky Header */
    .nav-container {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 80px;
        background-color: rgba(255, 255, 255, 0.95);
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 5%;
        z-index: 999;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    .logo-text {
        font-family: 'Playfair Display', serif;
        font-size: 24px;
        font-weight: 900;
        color: var(--deep-navy);
    }

    .logo-accent {
        color: var(--vibrant-orange);
    }

    /* Hero Section */
    .hero-container {
        position: relative;
        height: 80vh;
        width: 100%;
        background-image: linear-gradient(rgba(27, 46, 75, 0.6), rgba(27, 46, 75, 0.3)), url('https://images.unsplash.com/photo-1581578731548-c64695cc6958?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        color: white;
        margin-top: 0px;
        border-radius: 0 0 50px 50px;
    }

    .hero-title {
        font-size: 64px;
        font-weight: 900;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .hero-subtitle {
        font-size: 24px;
        font-weight: 300;
        max-width: 800px;
        margin-bottom: 40px;
    }

    /* Buttons */
    .btn-primary {
        background-color: var(--vibrant-orange);
        color: white !important;
        padding: 15px 35px;
        border-radius: 30px;
        font-weight: 600;
        text-decoration: none;
        transition: all 0.3s ease;
        display: inline-block;
        margin: 10px;
    }

    .btn-secondary {
        background-color: transparent;
        color: white !important;
        padding: 15px 35px;
        border-radius: 30px;
        font-weight: 600;
        text-decoration: none;
        border: 2px solid white;
        transition: all 0.3s ease;
        display: inline-block;
        margin: 10px;
    }

    .btn-primary:hover {
        background-color: #d46f08;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(245, 130, 10, 0.4);
    }

    /* WhatsApp Floating Button */
    .whatsapp-float {
        position: fixed;
        bottom: 40px;
        right: 40px;
        background-color: #25d366;
        color: white;
        width: 60px;
        height: 60px;
        border-radius: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 30px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        z-index: 1000;
        text-decoration: none;
    }

    /* Service Cards */
    .service-card {
        padding: 30px;
        border-radius: 20px;
        background: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        text-align: center;
        height: 100%;
        border: 1px solid #eee;
    }

    .service-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border-color: var(--lime-green);
    }

    .service-icon {
        font-size: 40px;
        margin-bottom: 20px;
        display: block;
    }

    /* Section Styles */
    .section-padding {
        padding: 100px 5%;
    }

    .section-title {
        text-align: center;
        margin-bottom: 60px;
    }

    .section-title h2 {
        font-size: 48px;
        margin-bottom: 20px;
    }

    .section-title p {
        color: #666;
        font-size: 18px;
    }

    /* Process Steps */
    .step-container {
        display: flex;
        justify-content: space-between;
        position: relative;
    }

    .step-item {
        flex: 1;
        text-align: center;
        padding: 20px;
        position: relative;
    }

    .step-number {
        width: 50px;
        height: 50px;
        background: var(--deep-navy);
        color: white;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: 700;
        margin: 0 auto 20px;
        position: relative;
        z-index: 2;
    }

    /* Testimonials */
    .testimonial-card {
        background: var(--soft-white);
        padding: 40px;
        border-radius: 25px;
        margin-bottom: 20px;
    }

    .stars {
        color: #FFD700;
        margin-bottom: 15px;
    }

    /* Footer */
    .footer {
        background: var(--deep-navy);
        color: white;
        padding: 80px 5% 40px;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .hero-title { font-size: 40px; }
        .hero-container { height: 60vh; }
        .nav-container { padding: 0 20px; }
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Sticky Header
st.markdown("""
<div class="nav-container">
    <div class="logo-text">EMMACULATE<span class="logo-accent">.</span></div>
    <div style="display: flex; align-items: center; gap: 20px;">
        <a href="#services" style="color: var(--deep-navy); text-decoration: none; font-weight: 600;">Services</a>
        <a href="#booking" class="btn-primary" style="padding: 10px 20px; font-size: 14px; margin: 0;">Book Now</a>
    </div>
</div>
""", unsafe_allow_html=True)

# 1. Hero Section
st.markdown("""
<div class="hero-container">
    <div style="font-family: 'Playfair Display', serif; font-size: 14px; letter-spacing: 4px; color: rgba(255,255,255,0.6); margin-bottom: 20px; text-transform: uppercase;">Emmaculate Cleaning Service</div>
    <h1 class="hero-title">Professional Cleaning <br>You Can Trust</h1>
    <p class="hero-subtitle">Residential, Commercial & Specialized Cleaning Services Delivered with Precision</p>
    <div>
        <a href="#booking" class="btn-primary">Request a Quote</a>
        <a href="https://wa.me/1234567890" class="btn-secondary">Chat on WhatsApp</a>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. Services Section
st.markdown("""
<div id="services" class="section-padding">
    <div class="section-title">
        <p>OUR SERVICES</p>
        <h2>Excellence in Every Corner</h2>
    </div>
    <div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;">
        <div style="flex: 1; min-width: 280px; max-width: 350px;">
            <div class="service-card">
                <span class="service-icon">🏠</span>
                <h3>Residential Cleaning</h3>
                <p>Personalized home cleaning tailored to your lifestyle and needs.</p>
            </div>
        </div>
        <div style="flex: 1; min-width: 280px; max-width: 350px;">
            <div class="service-card">
                <span class="service-icon">🏢</span>
                <h3>Commercial Cleaning</h3>
                <p>Professional workspace maintenance for a healthy and productive environment.</p>
            </div>
        </div>
        <div style="flex: 1; min-width: 280px; max-width: 350px;">
            <div class="service-card">
                <span class="service-icon">🏗️</span>
                <h3>Post-Construction</h3>
                <p>Thorough deep-cleaning to make your new space ready for immediate use.</p>
            </div>
        </div>
        <div style="flex: 1; min-width: 280px; max-width: 350px;">
            <div class="service-card">
                <span class="service-icon">🛋️</span>
                <h3>Upholstery Cleaning</h3>
                <p>Revitalize your furniture with our specialized deep-cleaning techniques.</p>
            </div>
        </div>
        <div style="flex: 1; min-width: 280px; max-width: 350px;">
            <div class="service-card">
                <span class="service-icon">🛡️</span>
                <h3>Mold Treatment</h3>
                <p>Professional removal and prevention of mold for a safer home environment.</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. Before & After Showcase
st.markdown("""
<div class="section-padding" style="background-color: var(--soft-white);">
    <div class="section-title">
        <p>TRANSFORMATIONS</p>
        <h2>See the Emmaculate Difference</h2>
    </div>
    <div style="display: flex; flex-wrap: wrap; gap: 30px; align-items: center;">
        <div style="flex: 1; min-width: 300px; border-radius: 20px; overflow: hidden; box-shadow: 0 15px 35px rgba(0,0,0,0.1);">
            <div style="position: relative;">
                <img src="https://images.unsplash.com/photo-1527515637462-cff94eecc1ac?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" style="width: 100%; display: block;" alt="Before and After">
                <div style="position: absolute; top: 20px; left: 20px; background: rgba(27, 46, 75, 0.8); color: white; padding: 5px 15px; border-radius: 10px; font-size: 12px;">BEFORE / AFTER</div>
            </div>
        </div>
        <div style="flex: 1; min-width: 300px;">
            <h3 style="font-size: 32px; margin-bottom: 20px;">Precision and Care <br>in Every Detail</h3>
            <p style="font-size: 18px; color: #666; line-height: 1.6;">Our team doesn't just clean; we restore. Using premium products and systematic techniques, we achieve results that you can see, feel, and smell.</p>
            <ul style="list-style: none; padding: 0;">
                <li style="margin-bottom: 15px; display: flex; align-items: center;"><span style="color: var(--lime-green); margin-right: 10px;">✓</span> Eco-friendly premium products</li>
                <li style="margin-bottom: 15px; display: flex; align-items: center;"><span style="color: var(--lime-green); margin-right: 10px;">✓</span> Specialized equipment for deep cleaning</li>
                <li style="margin-bottom: 15px; display: flex; align-items: center;"><span style="color: var(--lime-green); margin-right: 10px;">✓</span> 100% Satisfaction Guarantee</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. How It Works (Process Section)
st.markdown("""
<div class="section-padding">
    <div class="section-title">
        <p>HOW IT WORKS</p>
        <h2>Your Journey to a Spotless Space</h2>
    </div>
    <div class="step-container" style="flex-wrap: wrap;">
        <div class="step-item">
            <div class="step-number">1</div>
            <h4>Request a Quote</h4>
            <p style="font-size: 14px; color: #666;">Contact us via our form or WhatsApp with your cleaning needs.</p>
        </div>
        <div class="step-item">
            <div class="step-number">2</div>
            <h4>Site Assessment</h4>
            <p style="font-size: 14px; color: #666;">We provide a professional assessment to ensure an accurate quote.</p>
        </div>
        <div class="step-item">
            <div class="step-number">3</div>
            <h4>Receive Quote</h4>
            <p style="font-size: 14px; color: #666;">A transparent, detailed quote delivered within 24 hours.</p>
        </div>
        <div class="step-item">
            <div class="step-number">4</div>
            <h4>Book with Deposit</h4>
            <p style="font-size: 14px; color: #666;">Secure your preferred date with a flexible booking deposit.</p>
        </div>
        <div class="step-item">
            <div class="step-number">5</div>
            <h4>We Deliver</h4>
            <p style="font-size: 14px; color: #666;">Our expert team transforms your space to perfection.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 5. Testimonials / Client Trust
st.markdown("""
<div class="section-padding" style="background-color: var(--soft-white);">
    <div class="section-title">
        <p>CLIENT TRUST</p>
        <h2>Trusted by Modern Homeowners</h2>
    </div>
    <div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;">
        <div style="flex: 1; min-width: 300px; max-width: 400px;">
            <div class="testimonial-card">
                <div class="stars">★★★★★</div>
                <p style="font-style: italic; margin-bottom: 20px;">"The attention to detail was exceptional. I've used many cleaning services, but Emmaculate is truly in a league of its own."</p>
                <div style="display: flex; align-items: center;">
                    <div style="width: 40px; height: 40px; border-radius: 50%; background: #ddd; margin-right: 15px;"></div>
                    <div><strong>Sarah Johnson</strong><br><small>Residential Client</small></div>
                </div>
            </div>
        </div>
        <div style="flex: 1; min-width: 300px; max-width: 400px;">
            <div class="testimonial-card">
                <div class="stars">★★★★★</div>
                <p style="font-style: italic; margin-bottom: 20px;">"Reliable, professional, and thorough. Our office has never looked better. Highly recommend their commercial services."</p>
                <div style="display: flex; align-items: center;">
                    <div style="width: 40px; height: 40px; border-radius: 50%; background: #ddd; margin-right: 15px;"></div>
                    <div><strong>Mark Thompson</strong><br><small>Business Owner</small></div>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. Booking / Inquiry Section
st.markdown("<div id='booking' class='section-padding'>", unsafe_allow_html=True)
st.markdown("""
<div class="section-title">
    <p>GET IN TOUCH</p>
    <h2>Ready for a Fresh Start?</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    with st.form("quote_form"):
        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email Address")
        service = st.selectbox("Service Type", ["Residential Cleaning", "Commercial Cleaning", "Post-Construction", "Upholstery Cleaning", "Mold Treatment"])
        message = st.text_area("Your Message")

        submitted = st.form_submit_button("Get Your Quote")
        if submitted:
            st.success("Thank you! We'll respond quickly via WhatsApp or phone.")

with col2:
    st.markdown("""
    <div style="background: var(--deep-navy); color: white; padding: 40px; border-radius: 25px; height: 100%;">
        <h3>Quick Contact</h3>
        <p>Prefer to chat? Message us directly on WhatsApp for an instant response.</p>
        <br>
        <a href="https://wa.me/1234567890" class="btn-primary" style="margin: 0; width: 100%; text-align: center;">Message WhatsApp</a>
        <br><br><br>
        <p><strong>Support:</strong> info@emmaculate.com</p>
        <p><strong>Hours:</strong> Mon - Sat: 8am - 6pm</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# 7. Future Brand Teaser
st.markdown("""
<div class="section-padding" style="background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); text-align: center;">
    <div style="max-width: 800px; margin: 0 auto;">
        <p style="color: var(--lime-green); font-weight: 700; letter-spacing: 2px;">COMING SOON</p>
        <h2 style="font-size: 42px; margin-bottom: 20px;">Pure Tropics</h2>
        <p style="font-size: 20px; color: #666; margin-bottom: 30px;">Our exclusive line of eco-friendly, tropical-scented cleaning products is arriving soon. Nature's freshness, delivered to your doorstep.</p>
        <div style="display: inline-block; padding: 10px 30px; border: 2px dashed var(--lime-green); border-radius: 10px; color: var(--lime-green); font-weight: 600;">Coming Fall 2023</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 8. Footer
st.markdown("""
<div class="footer">
    <div style="display: flex; flex-wrap: wrap; gap: 40px; justify-content: space-between; margin-bottom: 60px;">
        <div style="flex: 1; min-width: 250px;">
            <div class="logo-text" style="color: white; margin-bottom: 20px;">EMMACULATE<span class="logo-accent">.</span></div>
            <p style="color: #ccc; line-height: 1.6;">Premium cleaning services for those who value precision and trust. We make your space immaculate.</p>
        </div>
        <div style="flex: 1; min-width: 200px;">
            <h4 style="color: white; margin-bottom: 20px;">Quick Links</h4>
            <ul style="list-style: none; padding: 0; color: #ccc;">
                <li style="margin-bottom: 10px;"><a href="#" style="color: #ccc; text-decoration: none;">Home</a></li>
                <li style="margin-bottom: 10px;"><a href="#services" style="color: #ccc; text-decoration: none;">Services</a></li>
                <li style="margin-bottom: 10px;"><a href="#booking" style="color: #ccc; text-decoration: none;">Book Now</a></li>
            </ul>
        </div>
        <div style="flex: 1; min-width: 250px;">
            <h4 style="color: white; margin-bottom: 20px;">Contact Us</h4>
            <p style="color: #ccc; margin-bottom: 10px;">📞 +1 (234) 567-890</p>
            <p style="color: #ccc; margin-bottom: 10px;">💬 WhatsApp: +1 (234) 567-890</p>
            <p style="color: #ccc; margin-bottom: 10px;">📧 info@emmaculate.com</p>
        </div>
    </div>
    <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 30px; display: flex; justify-content: space-between; flex-wrap: wrap; color: #888; font-size: 14px;">
        <p>© 2023 Emmaculate Cleaning Service. All rights reserved.</p>
        <p>Designed for Excellence</p>
    </div>
</div>
""", unsafe_allow_html=True)

# WhatsApp Float
st.markdown("""
<a href="https://wa.me/1234567890" class="whatsapp-float">
    <span style="display: flex; justify-content: center; align-items: center; height: 100%;">💬</span>
</a>
""", unsafe_allow_html=True)
