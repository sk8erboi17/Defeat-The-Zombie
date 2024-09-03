package it.sk8erboi.customproject.network.input;

public class ValidateHandler implements Handler{
    @Override
    public void handle(Object request) {
        if(request == null){
            throw new NullPointerException("Request cannot be null");
        }

    }
}
