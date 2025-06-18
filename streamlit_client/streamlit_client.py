# streamlit_client_gcp.py
import streamlit as st
import grpc
import os # Import os module

# Import the generated classes
import greeter_pb2
import greeter_pb2_grpc
from google.protobuf import empty_pb2

# --- App Configuration ---
# 💡 KEY CHANGE FOR CLOUD RUN: Get the server address from an environment variable.
# We will set this environment variable when we deploy the client.
SERVER_ADDRESS = os.environ.get("GRPC_SERVER_URL")

st.set_page_config(page_title="gRPC Client on GCP", layout="centered")


# --- Helper Function to Create gRPC Channel ---
def get_grpc_channel():
    """Creates a gRPC channel to connect to the server."""
    if not SERVER_ADDRESS:
        # This will be shown if the environment variable is not set.
        st.error("GRPC_SERVER_URL environment variable is not set!")
        st.stop()
    
    # 💡 KEY CHANGE FOR CLOUD RUN: Use a secure channel with default credentials.
    # Google Cloud Run provides a valid SSL certificate automatically.
    credentials = grpc.ssl_channel_credentials()
    return grpc.secure_channel(SERVER_ADDRESS, credentials)


# --- Streamlit UI ---
st.title("gRPC Client Tester on GCP ☁️")
if SERVER_ADDRESS:
    st.markdown(f"This app is a client for a gRPC server running at `{SERVER_ADDRESS}`.")
st.markdown("---")


# --- SayHello RPC Section ---
st.header("1. Call `SayHello` RPC")
user_name = st.text_input("Enter your name:", "Cloud Run")

if st.button("Send Greeting"):
    if not user_name:
        st.warning("Please enter a name.")
    else:
        st.info(f"Attempting to call `SayHello` on {SERVER_ADDRESS}...")
        try:
            with get_grpc_channel() as channel:
                stub = greeter_pb2_grpc.GreeterStub(channel)
                request = greeter_pb2.HelloRequest(name=user_name)
                response = stub.SayHello(request, timeout=10)
                st.success("✅ RPC call successful!")
                st.markdown("**Server Response:**")
                st.code(response.message, language="text")

        except grpc.RpcError as e:
            st.error("❌ An RPC error occurred!")
            status_code = e.code()
            st.write(f"**Status Code:** `{status_code.name}`")
            st.write(f"**Details:** {e.details()}")
            if status_code == grpc.StatusCode.UNAVAILABLE:
                st.warning("The server is unavailable. Check the URL and make sure the server is deployed and running correctly.")

# --- GetServerTime RPC Section is largely the same, so it's omitted for brevity but should be included in your file.
# (You can copy the GetServerTime section from the local client file)

