package it.sk8erboi.customproject.services;

import org.springframework.stereotype.Service;

import java.util.HashMap;

//a class for send the updates to the web server
@Service
public class LoggingService {

    private final HashMap<Object,Boolean> updates = new HashMap<>();

    public void addUpdate(Object object, boolean read) {
        updates.put(object,read);
    }

    public HashMap<Object,Boolean> getAllUpdates() {
        return updates;
    }
}
