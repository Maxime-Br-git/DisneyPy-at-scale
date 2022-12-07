FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests && pip3 install datetime
ADD test_permission_invalid.py /test/test_permission_invalid.py
ADD test_permission_valid.py /test/test_permission_valid.py
ADD test_performance.py /test/test_performance.py
ADD test_prediction_output.py /test/test_prediction_output.py
WORKDIR /test/
EXPOSE 5001
CMD python3 test_permission_invalid.py ; python3 test_permission_valid.py ; python3 test_performance.py; python3 test_prediction_output.py