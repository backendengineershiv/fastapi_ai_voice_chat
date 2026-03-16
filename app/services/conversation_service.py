from app.database.mongodb import conversation_collection


async def save_message(session_id, role, content):

    await conversation_collection.update_one(
        {"session_id": session_id},
        {
            "$push": {
                "messages": {
                    "role": role,
                    "content": content
                }
            }
        },
        upsert=True
    )

async def get_messages(session_id):

    convo = await conversation_collection.find_one(
        {"session_id": session_id}
    )

    if convo and "messages" in convo:
        return convo["messages"]

    return []