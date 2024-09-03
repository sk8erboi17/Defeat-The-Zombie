package it.sk8erboi.customproject.services;

import it.sk8erboi.customproject.world.User;
import org.springframework.stereotype.Component;

import java.nio.channels.AsynchronousSocketChannel;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;


@Component
public class NetworkService {

    private final CopyOnWriteArrayList<User> userArrayList = new CopyOnWriteArrayList<>();

    //add user to the network
    public void addUser(User user){

        //check if the connection is avaible
        if(user.getAsynchronousSocketChannel() == null) {
            throw new NullPointerException("AsynchronousSocketChannel is null");
        }

        //add user
        userArrayList.add(user);

    }

    //get user
    public User getUserByName(String name){
        return userArrayList.stream().filter(user -> user.getUsername().equalsIgnoreCase(name)).findFirst().orElseThrow(() -> new NullPointerException("User not found"));
    }

    //remove user
    public void removeUser(AsynchronousSocketChannel asynchronousSocketChannel){
        //check if the connection is avaible
        if(asynchronousSocketChannel != null) {
            System.out.println(getByAsyncSocketChannel(asynchronousSocketChannel).getUsername() + " disconnected!");
            //remove user
            userArrayList.remove(getByAsyncSocketChannel(asynchronousSocketChannel));

        }
    }

    public User getByAsyncSocketChannel(AsynchronousSocketChannel asynchronousSocketChannel){
        return userArrayList.stream().filter(user -> user.getAsynchronousSocketChannel().equals(asynchronousSocketChannel)).findFirst().orElseThrow(() -> new NullPointerException("User not found"));
    }


    public CopyOnWriteArrayList<User> getUserList(){
        return userArrayList;
    }
}
