package it.sk8erboi.customproject.api.network.pipeline.in;

import it.sk8erboi.customproject.api.listeners.response.Callback;
import it.sk8erboi.customproject.api.network.AggregateCallback;
import it.sk8erboi.customproject.services.NetworkService;

import java.nio.channels.AsynchronousSocketChannel;
import java.util.List;

/**
 * The PipelineInBuilder class is a builder class for constructing a PipelineIn object.
 * It provides a flexible and fluent API for setting various configurations required to create a PipelineIn instance,
 * including buffer size, direct buffer allocation, and callbacks.
 */
public class PipelineInBuilder {

    private final AsynchronousSocketChannel client;
    private boolean allocateDirect = false;
    private int bufferSize = 4096;
    private AggregateCallback aggregateCallback;
    private NetworkService networkService;

    public PipelineInBuilder(AsynchronousSocketChannel client) {
        this.client = client;
    }

    public PipelineInBuilder configureAggregateCallback(List<Callback> callbacks) {
        this.aggregateCallback = new AggregateCallback(callbacks);
        return this;
    }

    public PipelineInBuilder setBufferSize(int bufferSize) {
        this.bufferSize = bufferSize;
        return this;
    }

    public PipelineInBuilder allocateDirect(boolean allocateDirect) {
        this.allocateDirect = allocateDirect;
        return this;
    }

    public PipelineInBuilder setNetworkService(NetworkService networkService) {
        this.networkService = networkService;
        return this;
    }
    public PipelineIn build() {
        return new PipelineIn(client, allocateDirect, bufferSize, aggregateCallback,networkService);
    }


}
