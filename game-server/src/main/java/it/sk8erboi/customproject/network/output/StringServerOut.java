package it.sk8erboi.customproject.network.output;

import it.sk8erboi.customproject.api.listeners.response.Callback;
import it.sk8erboi.customproject.api.listeners.response.CallbackBuilder;
import it.sk8erboi.customproject.api.network.pipeline.out.content.Request;

//the packets to send to the client
public class StringServerOut implements Request {
    private final String message;

    public StringServerOut(String message) {
        this.message = message;
    }

    @Override
    public Object getMessage() {
        return message;
    }

    @Override
    public Callback getCallback() {
        return new CallbackBuilder()
                .onComplete(null)
                .onException(Throwable::printStackTrace).build();
    }
}