import qrcode
import streamlit as st
from io import BytesIO
from PIL import Image
import numpy as np

# Initialize session state for reset functionality
if 'reset' not in st.session_state:
    st.session_state.reset = False

# Set page configuration
st.set_page_config(page_title="QR Code Generator Pro", layout="centered")
st.title(" Custom QR Code Generator WebApp")

# Reset function
def reset_settings():
    st.session_state.data = "https://github.com/Crashlar1"
    st.session_state.fill_color = "#000000"
    st.session_state.back_color = "#FFFFFF"
    st.session_state.error_correction = "L (Low)"
    st.session_state.box_size = 10
    st.session_state.border = 4
    st.session_state.auto_version = True
    st.session_state.animated = False
    st.session_state.frames = 5
    st.session_state.duration = 200

# Main input section
with st.form("qr_form"):
    # Reset button
    st.form_submit_button("🔄 Reset Settings", on_click=reset_settings)
    
    st.subheader(" Content Configuration")
    data = st.text_input("Text/URL:", 
                        value="https://www.linkedin.com/in/crashlar/", 
                        placeholder="Enter text or URL here",
                        key="data")
    
    st.subheader(" Customization Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎨 Colors**")
        fill_color = st.color_picker("Foreground Color", "#000000", key="fill_color")
        back_color = st.color_picker("Background Color", "#FFFFFF", key="back_color")
        
    with col2:
        st.markdown("** Advanced Settings**")
        error_correction = st.selectbox("Error Correction", 
                                       ["L (Low)", "M (Medium)", "Q (Quartile)", "H (High)"], 
                                       index=0, key="error_correction")
        box_size = st.slider("Module Size", 5, 20, 10, key="box_size")
        border = st.slider("Border Width", 1, 10, 4, key="border")
        auto_version = st.checkbox("Auto Version", True, key="auto_version")
    
    st.subheader("🎥 Animation Options")
    animated = st.checkbox("Generate Animated QR Code", False, key="animated")
    
    if animated:
        col3, col4 = st.columns(2)
        with col3:
            frames = st.slider("Number of Frames", 3, 20, 5, key="frames")
        with col4:
            duration = st.slider("Frame Duration (ms)", 100, 1000, 200, key="duration")

    generate = st.form_submit_button(" Generate QR Code")

# Error correction mapping
ec_mapping = {
    "L (Low)": qrcode.constants.ERROR_CORRECT_L,
    "M (Medium)": qrcode.constants.ERROR_CORRECT_M,
    "Q (Quartile)": qrcode.constants.ERROR_CORRECT_Q,
    "H (High)": qrcode.constants.ERROR_CORRECT_H,
}

def generate_animated_qr(data, base_color, frames=5, duration=200, **kwargs):
    images = []
    for i in range(frames):
        # Create color gradient
        hue = (i / frames) * 360
        frame_color = f"hsl({hue}, 100%, 50%)"
        
        qr = qrcode.QRCode(**kwargs)
        qr.add_data(data)
        qr.make(fit=kwargs.get('version', None))
        
        img = qr.make_image(fill_color=frame_color, back_color=base_color)
        images.append(img.get_image())
    return images, duration

if generate:
    if not data:
        st.warning(" Please enter some text or URL!")
    else:
        try:
            qr_params = {
                'version': None if st.session_state.auto_version else 1,
                'error_correction': ec_mapping[st.session_state.error_correction],
                'box_size': st.session_state.box_size,
                'border': st.session_state.border
            }

            if animated:
                # Generate animated QR code
                frames, duration = generate_animated_qr(
                    data,
                    st.session_state.back_color,
                    frames=st.session_state.frames,
                    duration=st.session_state.duration,
                    **qr_params
                )
                
                # Save as GIF
                buf = BytesIO()
                frames[0].save(buf, 
                               format='GIF', 
                               save_all=True, 
                               append_images=frames[1:], 
                               duration=duration, 
                               loop=0)
                qr_img = buf.getvalue()
                
                file_name = "animated_qrcode.gif"
                mime_type = "image/gif"
            else:
                # Generate static QR code
                qr = qrcode.QRCode(**qr_params)
                qr.add_data(data)
                qr.make(fit=st.session_state.auto_version)
                
                img = qr.make_image(fill_color=st.session_state.fill_color, 
                                  back_color=st.session_state.back_color)
                
                # Convert to bytes
                buf = BytesIO()
                img.save(buf, format="PNG")
                qr_img = buf.getvalue()
                
                file_name = "custom_qrcode.png"
                mime_type = "image/png"

            # Display results
            st.success(" QR Code Generated Successfully!")
            
            col_left, col_right = st.columns([1, 2])
            
            with col_left:
                st.download_button(
                    label=" Download Your QR Code",
                    data=qr_img,
                    file_name=file_name,
                    mime=mime_type,
                )
                
                st.markdown("** Technical Details**")
                st.write(f"Format: {'Animated GIF' if animated else 'PNG'}")
                if animated:
                    st.write(f"Frames: {st.session_state.frames}")
                    st.write(f"Duration: {st.session_state.duration}ms per frame")
                st.write(f"Version: {qr.version if 'qr' in locals() else 'Auto'}")
                st.write(f"Error Correction: {st.session_state.error_correction.split()[0]}")
                st.write(f"Module Size: {st.session_state.box_size}px")
                st.write(f"Border Width: {st.session_state.border} modules")
                
            with col_right:
                st.image(qr_img, caption="Powered by You", use_column_width=True)
            
        except Exception as e:
            st.error(f" Error generating QR code: {str(e)}")
