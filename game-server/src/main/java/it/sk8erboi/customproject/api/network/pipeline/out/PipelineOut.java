package it.sk8erboi.customproject.api.network.pipeline.out;

import it.sk8erboi.customproject.api.listeners.output.AsyncDataSender;
import it.sk8erboi.customproject.api.network.pipeline.out.content.Request;

import java.nio.channels.AsynchronousSocketChannel;

/**
 * The PipelineOut class is responsible for managing the output pipeline for sending various types of data to a client using asynchronous operations.
 * It utilizes an AsyncDataSender to handle data transmission based on the type of data requested.
 */
public class PipelineOut {
    private final AsynchronousSocketChannel client;

    private final boolean allocateDirect;

    private final int initBuffer;

    public PipelineOut(AsynchronousSocketChannel client, boolean allocateDirect, int initBuffer) {
        this.client = client;
        this.allocateDirect = allocateDirect;
        this.initBuffer = initBuffer;
    }


    public void handleRequest(Request request) {
        AsyncDataSender asyncDataSender = new AsyncDataSender(client, initBuffer, allocateDirect);
        Object message = request.getMessage();
        switch (message) {
            case String s -> asyncDataSender.sendString(s, request.getCallback());
            case Integer i -> asyncDataSender.sendInt(i, request.getCallback());
            case Float v -> asyncDataSender.sendFloat(v, request.getCallback());
            case Double v -> asyncDataSender.sendDouble(v, request.getCallback());
            case Character c -> asyncDataSender.sendChar(c, request.getCallback());
            case byte[] bytes -> asyncDataSender.sendByteArray(bytes, request.getCallback());
            case null, default -> System.err.println("Unsupported message type: " + message.getClass().getSimpleName());
        }
    }

}
