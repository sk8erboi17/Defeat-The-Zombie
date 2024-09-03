package it.sk8erboi.customproject.api.network.pipeline.in;

import it.sk8erboi.customproject.api.BufferBuilder;
import it.sk8erboi.customproject.api.listeners.input.AsyncDataReceiver;
import it.sk8erboi.customproject.api.listeners.response.Callback;
import it.sk8erboi.customproject.services.NetworkService;

import java.nio.channels.AsynchronousSocketChannel;

/**
 * The PipelineIn class manages the process of reading data from a client connection using an asynchronous data receiver. It initializes the data receiver with the necessary configurations and starts the reading process using a buffer.
 */
public class PipelineIn {

    // Constructor to initialize and start reading data
    public PipelineIn(AsynchronousSocketChannel client, boolean allocateDirect, int bufferSize, Callback callback, NetworkService networkService) {
        AsyncDataReceiver asyncDataReceiver = new AsyncDataReceiver(client, bufferSize, callback,networkService);
        // Start reading data using a buffer created with BufferBuilder
        asyncDataReceiver.startRead(new BufferBuilder().setInitSize(bufferSize).allocateDirect(allocateDirect).build());
    }

}
