from core.scraper import validate_image
import os

def test_image_validation():
    # Test with a known valid image (Google logo)
    url = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
    valid, reason = validate_image(url)
    print(f"Valid: {valid}, Reason: {reason}")
    # Google logo is 544x184 (2x), so it should be valid since > 200x200 might be tight on height
    # Wait, the requirement was 200x200 minimum. 92dp * 2 = 184. 184 < 200.
    # So it SHOULD be invalid based on my 200x200 rule.

    # Let's try a larger one
    url_large = "https://via.placeholder.com/300"
    valid_l, reason_l = validate_image(url_large)
    print(f"Large Valid: {valid_l}, Reason: {reason_l}")

    # Test invalid content type
    url_text = "https://www.google.com"
    valid_t, reason_t = validate_image(url_text)
    print(f"Text Valid: {valid_t}, Reason: {reason_t}")
    assert not valid_t

    print("Image validation test completed!")

if __name__ == "__main__":
    test_image_validation()
