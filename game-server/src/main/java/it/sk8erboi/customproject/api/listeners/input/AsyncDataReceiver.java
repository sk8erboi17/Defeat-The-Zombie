package it.sk8erboi.customproject.api.listeners.input;

import it.sk8erboi.customproject.api.exception.MaxBufferSizeExceededException;
import it.sk8erboi.customproject.api.listeners.input.operations.ListenData;
import it.sk8erboi.customproject.api.listeners.output.AsyncChannelSocket;
import it.sk8erboi.customproject.api.listeners.response.Callback;
import it.sk8erboi.customproject.services.NetworkService;
import it.sk8erboi.customproject.world.User;

import java.nio.ByteBuffer;
import java.nio.channels.AsynchronousSocketChannel;
import java.nio.channels.CompletionHandler;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * On the server side, InputListener handles the reception of data from the client.
 * It reads data from the AsynchronousSocketChannel into a ByteBuffer
 */

public class AsyncDataReceiver implements CompletionHandler<Integer, ByteBuffer> {

    private final ExecutorService readThread;
    private final ListenData processData;
    private final AsynchronousSocketChannel socketChannel;
    private final int bufferSize;
    private final Callback callback;
    private final NetworkService networkService;

    public AsyncDataReceiver(AsynchronousSocketChannel socketChannel, int bufferSize, Callback callback, NetworkService networkService) {
        this.socketChannel = socketChannel;
        this.callback = callback;
        this.bufferSize = bufferSize;
        this.networkService = networkService;
        this.readThread = Executors.newScheduledThreadPool(Runtime.getRuntime().availableProcessors() / 2);
        this.processData = new ListenData();
    }

    @Override
    public void completed(Integer bytesRead, ByteBuffer buffer) {
        // This method is called when data is successfully read from the channel

        if (bytesRead < 0) { // Check if end of stream is reached
            AsyncChannelSocket.closeChannelSocketChannel(socketChannel);
            throw new RuntimeException("Not enough byte to read");
        }

        // If the buffer has filled up beyond the allowed size, close the channel and throw error
        if (buffer.remaining() >= bufferSize) {
            AsyncChannelSocket.closeChannelSocketChannel(socketChannel);
            try {
                throw new MaxBufferSizeExceededException();
            } catch (MaxBufferSizeExceededException e) {
                e.printStackTrace();
            }
            return;
        }

        buffer.flip(); // Prepare the buffer for reading
        send(buffer);  // Process the data in the buffer
        buffer.clear(); // Clear the buffer for the next read

        // Execute the next read operation in a separate thread
        readThread.execute(() -> startRead(buffer));
    }

    // Method to process the data in the buffer using ListenData
    private void send(ByteBuffer buffer) {
        processData.listen(buffer, callback);
    }

    // Method to start reading data into the buffer
    public void startRead(ByteBuffer buffer) {
        socketChannel.read(buffer, buffer, this);
    }

    @Override
    public void failed(Throwable exc, ByteBuffer buffer) {
        // This method is called if the read operation fails
        networkService.removeUser(socketChannel);
        AsyncChannelSocket.closeChannelSocketChannel(socketChannel);
    }
}
