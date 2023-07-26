# Autoblocks Replays

This repository demonstrates how to integrate LLM chain replays into your code review process. It contains:

* a [`simpleaichat`](https://github.com/minimaxir/simpleaichat) application that uses the [Autoblocks Python SDK](https://github.com/autoblocksai/python-sdk) to send events to the Autoblocks API
* a GitHub Actions workflow that **replays** real, past events from end users on every push to a feature branch

With our GitHub integration enabled, your teammates are not only reviewing your code, but also the impact that code will have on your LLM chains, and therefore your end users.

<img width="1159" alt="Screenshot 2023-07-23 at 11 02 18 AM" src="https://github.com/autoblocksai/actions/assets/7498009/80055f36-a310-4056-8ac3-f2f0e4ac2b3f">

Unlike other solutions for testing LLMs, Autoblocks Replays are end-to-end. They test your LLM chains from the moment a user sends an input to your application to the moment your application sends a response to the user. This means you can not only review changes to the final response to the user, but also any intermediate steps that might have
changed along the way. This is especially useful for complicated chains that involve multiple services and multiple steps, e.g. if you're using a vector database, tool selection, etc. If you are only ever looking at the final response, it is hard to know which of the intermediate steps in your chain is causing the change.

## Examples

### Updating `simpleaichat`'s `character` input to `"Michael Scott"`

* [Pull request](https://github.com/autoblocksai/demo-replays/pull/6)
* [Replay results](https://github.com/autoblocksai/demo-replays/pull/6#issuecomment-1652606398)

<img width="1062" alt="Screenshot 2023-07-26 at 6 24 27 PM" src="https://github.com/autoblocksai/actions/assets/7498009/ef1b5e70-c2c0-41b8-a52b-af73cdcca11c">

This small change leads to a large change in the final response to the user:

<img width="1073" alt="Screenshot 2023-07-26 at 6 44 16 PM" src="https://github.com/autoblocksai/actions/assets/7498009/1b14f6cb-d666-42a5-a37e-dcfe3ea96742">

It also doesn't sound like Michael Scott from The Office. Digging into the intermediate steps, we can see `simpleaichat` updated the prompt with character instructions, but with the wrong Michael Scott:

<img width="979" alt="Screenshot 2023-07-26 at 6 46 32 PM" src="https://github.com/autoblocksai/actions/assets/7498009/ebad9b66-be9b-4f0c-b189-f362dd2a9956">

### Increasing the `temperature` parameter

* [Pull request](https://github.com/autoblocksai/demo-replays/pull/7)
* [Replay results](https://github.com/autoblocksai/demo-replays/pull/7#issuecomment-1652649904)

<img width="967" alt="Screenshot 2023-07-26 at 6 57 27 PM" src="https://github.com/autoblocksai/actions/assets/7498009/1825db5a-84b9-4bfc-bd28-faa2008ddfd4">

This change has pretty inoccuous results on the final response to the user. The model
changes a few words here and there, but the messaging is very similar.

Query about San Francisco:

<img width="1213" alt="Screenshot 2023-07-26 at 6 59 17 PM" src="https://github.com/autoblocksai/actions/assets/7498009/69ded03a-2d29-4287-b014-e6385526a1e6">

Query about highest points:

<img width="941" alt="Screenshot 2023-07-26 at 7 00 13 PM" src="https://github.com/autoblocksai/actions/assets/7498009/b68f5ac9-296f-4935-85dd-5b74e2c7e551">

### Changing the description of the tools

* [Pull request](https://github.com/autoblocksai/demo-replays/pull/2)
* [Replay results](https://github.com/autoblocksai/demo-replays/pull/2#issuecomment-1652129031)

Autoblocks helps you better understand how your code changes affect the intermediate steps in your chain, especially if you're using a wrapper like `simpleaichat` or `LangChain`, both of which are higher level wrappers around calls to LLMs. For example, perhaps a teammate has not fully read the `simpleaichat` documentation and doesn't realize that the
doc strings of the functions passed to the `tools` array are actually used in the prompts!

<img width="1058" alt="Screenshot 2023-07-26 at 7 12 01 PM" src="https://github.com/autoblocksai/actions/assets/7498009/204bfde2-86b4-487e-b92f-86ecacbf4d00">

Autoblocks would easily surface this change during the code review process:

<img width="1071" alt="Screenshot 2023-07-26 at 7 11 28 PM" src="https://github.com/autoblocksai/actions/assets/7498009/5f6117ce-d24e-488f-99f2-256f3115f741">

## Replaying Locally

Start the application with replays enabled:

```bash
AUTOBLOCKS_REPLAYS_ENABLED=true poetry run start
```

In another terminal, set the `AUTOBLOCKS_API_KEY` environment variable:

```bash
export AUTOBLOCKS_API_KEY=my-api-key
```

Then replay traces from a view:

```bash
poetry run replay --view-id clkeamsei0001l908cmjjtqrf --num-traces 3
```

```
Your replay id is 2023-07-23_09-36-36

Replaying event {'id': 'geepag24zence2kbe0ppagt9', 'traceId': '7cb3ec98-b320-4e62-9a51-b15d0218ae4c', 'timestamp': '2023-07-22T18:32:51.862Z', 'message': 'request.payload', 'properties': {'payload': {'query': 'What are all of the airports in London?'}, 'source': 'DEMO_REPLAYS'}}
```

The original and replayed traces are written to the `autoblocks-replays/` folder with the structure:

```
autoblocks-replays/
    <replay-id>/
        <trace-id>/
            original/
                <event-number>-<message>.json
            replayed/
                <event-number>-<message>.json
```

<img width="981" alt="Screenshot 2023-07-23 at 10 06 39 AM" src="https://github.com/autoblocksai/actions/assets/7498009/ce20918f-ce75-4cd3-a5d2-66d3e1a00914">

Inspect the original vs replayed output manually or use a CLI tool like `diff` to surface differences:

```
diff \
  autoblocks-replays/2023-07-23_09-36-36/7cb3ec98-b320-4e62-9a51-b15d0218ae4c/original \
  autoblocks-replays/2023-07-23_09-36-36/7cb3ec98-b320-4e62-9a51-b15d0218ae4c/replayed
```

<img width="799" alt="Screenshot 2023-07-22 at 2 39 47 PM" src="https://github.com/autoblocksai/actions/assets/7498009/4279db15-26fc-4346-8e16-1ed060bcd9f7">

## Replaying in GitHub Actions

Use the [`autoblocksai/actions/replay`](https://github.com/autoblocksai/actions/tree/main/replay) action to replay events in a GitHub Actions workflow. This is similar to replaying events locally but allows you to automate replays in your CI workflow and view results in the GitHub UI.

The action will leave a comment on your pull request with a summary of the replay results:

<img width="857" alt="Screenshot 2023-07-26 at 6 50 31 PM" src="https://github.com/autoblocksai/actions/assets/7498009/ebfb31da-af70-45bf-b9b5-5e640a4fa104">
