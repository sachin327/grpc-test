# grpc_server_gcp.py
from concurrent import futures
import time
import datetime
import grpc
import os # Import os module

# Import the generated classes
import greeter_pb2
import greeter_pb2_grpc
from google.protobuf import empty_pb2

# Create a class to define the server functions
class Greeter(greeter_pb2_grpc.GreeterServicer):

    # This function is called when a client calls the SayHello RPC
    def SayHello(self, request, context):
        print("--- SayHello RPC called ---")
        print(f"Received name: '{request.name}'")
        response_message = f"Hello, {request.name}! Greetings from the GCP-deployed gRPC server."
        response = greeter_pb2.HelloReply(message=response_message)
        print(f"Sending response: '{response_message}'")
        print("---------------------------\n")
        return response

    # This function is called when a client calls the GetServerTime RPC
    def GetServerTime(self, request, context):
        print("--- GetServerTime RPC called ---")
        now = datetime.datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S UTC")
        response = greeter_pb2.TimeReply(current_time=time_str)
        print(f"Sending current time: {time_str}")
        print("------------------------------\n")
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greeter_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    # 💡 KEY CHANGE FOR CLOUD RUN: Get port from environment variable, default to 8080
    port = os.environ.get("PORT", "8080")
    
    # 💡 KEY CHANGE FOR CLOUD RUN: Listen on all network interfaces
    server.add_insecure_port(f"[::]:{port}")
    
    server.start()
    print(f"✅ gRPC Server started and listening on port {port}.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
