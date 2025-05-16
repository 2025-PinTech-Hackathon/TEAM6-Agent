from agent.local_server.controllers.webSocketManager import websocket_manager


async def send_result_to_client(agent):
    history = agent.state.history

    if not hasattr(history, "all_results") or not history.all_results:
        return

    last_result = history.all_results[-1]
    print(last_result.model_dump())
    await websocket_manager.send_to_all(last_result.model_dump())
