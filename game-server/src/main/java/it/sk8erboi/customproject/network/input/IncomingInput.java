package it.sk8erboi.customproject.network.input;

import it.sk8erboi.customproject.api.Listener;
import it.sk8erboi.customproject.api.listeners.response.CallbackBuilder;
import it.sk8erboi.customproject.api.network.pipeline.in.PipelineInBuilder;
import it.sk8erboi.customproject.services.EnemyService;
import it.sk8erboi.customproject.services.NetworkService;
import it.sk8erboi.customproject.services.LoggingService;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.nio.channels.AsynchronousServerSocketChannel;
import java.util.List;

@Component
public class IncomingInput {

    @Autowired
    private NetworkService networkService;

    @Autowired
    private AsynchronousServerSocketChannel server;

    @Autowired
    private Listener listener;

    @Autowired
    private LoggingService loggingService;

    @Autowired
    private EnemyService enemyService;

    @PostConstruct
    public void incomeInput(){
        listener.startConnectionListen(server, client -> new PipelineInBuilder(client).configureAggregateCallback(
                        List.of(

                                //validate the request
                                new CallbackBuilder()
                                        .onComplete((object) -> new ValidateHandler().handle(object))
                                        .onException(Throwable::printStackTrace)
                                        .build(),

                                //handler user join
                                new CallbackBuilder()
                                        .onComplete((object) -> new JoinHandler(client,networkService, loggingService).handle(object))
                                        .onException(Throwable::printStackTrace)
                                        .build(),

                                //handle user kill
                                new CallbackBuilder()
                                        .onComplete((object) -> new KillHandler(loggingService,networkService,enemyService).handle(object))
                                        .onException(Throwable::printStackTrace)
                                        .build(),

                                //handle user movement
                                new CallbackBuilder()
                                        .onComplete((object) -> new MovementHandler(networkService).handle(object))
                                        .onException(Throwable::printStackTrace)
                                        .build()
                                       )).setBufferSize(65536).setNetworkService(networkService).build());
    }


}
