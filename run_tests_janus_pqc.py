import sys
from tests.test_black_box_janus_pqc import test_many_random_messages, test_tamper_detection

if __name__ == "__main__":
    try:
        test_many_random_messages(50)
        test_tamper_detection()
        print("All Janus_PQC black-box tests passed.")
    except AssertionError:
        print("A test failed.")
        sys.exit(1)
