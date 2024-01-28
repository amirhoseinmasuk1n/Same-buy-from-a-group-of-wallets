import asyncio
import aiohttp
import json
from collections import Counter
from datetime import datetime, timedelta
import random

MAX_CONCURRENT_REQUESTS = 100  # Adjust the number of concurrent requests
API_KEYS = ['J1Z5DPIB2NHUUEMJ9TP39DW76IBWCXTP37', 'N3ANQ4VM55HQMZ1Y1H19CQKYIVTUNIHN38', '7SU4XC3HG99CSEZUM7B42D4F73AQIEA7ZP']
wallet_addresses = [
    "0x9Cd6140c2De8AF7595629bCcA099497f0c28B2A9",
"0xad32180582cbd0770a8ffcef1d735ff31cbcd94f",
"0x65c6ad24460944f0e6878e5dc4b007e0dd093590",
"0x1b1E1d7c62DC1c5655562286f8f4BE57c6A309fB",
"0x9ABDe6fAe4c59D730A73142542d9a908BD291644",
"0xcb0a19dcae1d15b0c59885d146e3ffe2a5dd1a1b",
"0x8bc924a4c07b4369a58cf35f6dc3ba16c41fc999",
"0xc8cae545aeebf1a93ad6fe8b2cf019040eb37f8f",
"0x30D674022885E084aCAD98C1C26eFe91Fe39D0f7",
"0x6f1759179772e2ea2f63509112d5baed36c66f16",
"0xa43c750d5de3bd88ee4f35def72cf76afebec274",
"0x6313cc5cd6a88dfbf40ba134eb2df3242ac37f3d",
"0x0740e94c992eaf797e69276b2e87d03bcd12a802",
"0x9badae7a4a9030d094b799f13b306d2f462f9be9",
"0x1effd55a8646f7dc67c7578c20ce575cefeb1120",
"0xacce55c3def1f9af8fdfb9a6c4a1b249063c09ff",
"0x9f3456016d3D5d7066a8B7d2138515D733553cb2",
"0xd6d0a2aec48f66707ad4da8b21eccab94497bd89",
"0x92928fe008ed635aa822a5cadf0cba340d754a66",
"0x17fc5b4a38604afddc6f50578bcbc5de0b94333f",
"0xed660e8d8585d0e87fda16e52dcd9fdf4bca60b8",
"0xe82df0fc0bdf42c9b422afaad4ef98af0b0e6587",
"0xdb22ca143f6396ad289c79cdfa5cc47f65884162",
"0x00000012616b0cb849db9a897bc338b709bc56e5",
"0xa207e7fc9ea6ab628115fdb64b50a298fb046ebd",
"0x535f1fcdd9c5001d847b2e7ef579d6e4ab6f860b",
"0xbd579c4f7886bfdda1b5e3459f2ffb77d3741132",
"0xdbdb692ef06dfe10f609a9c0eab4b038d60b4243",
"0xccc7ff136024d283d73c6cc0fe372c6b712cfec6",
"0x1919e128d6163724abc4bcffb6c16130e2bae817",
"0x966c5496e978621b24db1177187ff1f9a02f4b9f",
"0xdc0b688033ae1ac996ac1dd95d37f0d52d21ff0a",
"0xca92187f1eeeef4aa8c7ba246e98249effa0f346",
"0x17Bc55276D07E506851FE0F1d1597f7f0B875eb1",
"0x0b8f4c4e7626a91460dac057eb43e0de59d5b44f",
"0x2581cc6ed9908c97fd9228340534bb6c2984b5e1",
"0x2b66f0ae7234ec4fe5d616989f4f6e8fc2a809d4",
"0xaee2ae13ebf81d38df5a9ed7013e80ea3f72e39b",
"0xc41f3d8a635fa04d2ba518b3da5a1a08c1ec9fca",
"0x88529d2289d47e9339938f25f2e56a33c91671cb",
"0x8eaf80a722bd6d4c7dd379f7fec1122be26b06ef",
"0x7a9803f2450e948f63bba32834792ce7aab02515",
"0x9ecad9d9d3ed0938cc3b84732d3ffa8ece3a87c8",
"0xefa9268490bb76d6b17793905473fefc03b5c824",
"0x275121b5734bdae3bd97da0fe37f47450656cb13",
"0xb0a1be32df8c8248a54389af5d5528c38d92d5be",
"0x901b676e27fa9ced94dcea48f73c97780b908311",
"0x59423e089f6770a09d1869b4544e8993f250d1f2",
"0x14439dbe3eacf79d66d11d866a38fff52fe67fac",
"0x303425052e462dd0f3044aee17e1f5be9c7de783",
"0x1d91da30b083fc17c5cda25b25819d4b8db27862",
"0x0e32D10aAF0ab37ac85CcfCF3beAC785E06D023D",
"0x37e38E229ecEBBf9a6F4B8479B71508Ece16D597",
"0x30615450f0de4188f9635dd3cf1f5648edf638b8",
"0x93764f433f1eff622f9b7649272e14c5780a929d",
"0xf6b2f420060578d0628275152659e12c2181fa85",
"0x092be6201950893794d650ac4c47f0c2e8169987",
"0x9dda370f43567b9c757a3f946705567bce482c42",
"0x1AF331dc34dD7C5C62AF28B5685328318b61888a",
"0xe8D3c311912513aE9Cc34016db69Eae9e9F4E2cC",
"0x22330AEc3060C6cfBc5C26c6E3bf9737241e7db2",
"0x4a2C786651229175407d3A2D405d1998bcf40614",
"0xAf2358e98683265cBd3a48509123d390dDf54534",
"0x711281c1b26aaed86e40e4caaf76c1962b45e161",
"0x7431931094e8bae1ecaa7d0b57d2284e121f760e",
"0x287e2c76aab4720786076c3deedd7dd386092050",
"0x9e4a9b4334f3167bc7dd35f48f2238c73f532baf",
"0x64aec4326d32499e9d38a40e22bbab1f2b74a848",
]
async def fetch(session, url, cache):f
    if url in cache:
        return cache[url]
    async with session.get(url) as response:
        data = await response.text()
        cache[url] = data
        return data

async def get_approval_transaction_hashes(api_key, wallet_address, cache):
    current_time = int(datetime.now().timestamp())
    twenty_four_hours_ago = int((datetime.now() - timedelta(hours=24)).timestamp())

    base_url = f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&startBlock=0&endBlock=99999999&sort=desc&apikey={api_key}&page=1&offset=10000"
    async with aiohttp.ClientSession() as session:
        response_text = await fetch(session, base_url, cache)
    data = json.loads(response_text)
    if 'status' in data and data['status'] == "1":
        transactions = data['result']
        approval_hashes = [tx['hash'] for tx in transactions if int(tx['timeStamp']) >= twenty_four_hours_ago and tx['input'].startswith('0x095ea7b3')]
        return approval_hashes
    else:
        print("Error:", data['message'])
        return []

async def get_token_contract_addresses(api_key, tx_hashes, cache):
    all_contract_addresses = []
    for tx_hash in tx_hashes:
        base_url = f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionReceipt&txhash={tx_hash}&apikey={api_key}"
        async with aiohttp.ClientSession() as session:
            response_text = await fetch(session, base_url, cache)
        data = json.loads(response_text)
        if 'error' in data:
            print(f"Error for transaction hash {tx_hash}: {data['error']['message']}")
            continue
        if 'result' not in data or 'logs' not in data['result']:
            print(f"No logs found in the response for transaction hash {tx_hash}")
            continue

        logs = data['result']['logs']
        specific_contract = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'.lower()
        contract_addresses = list({log['address'].lower() for log in logs if log['address'].lower() != specific_contract})
        all_contract_addresses.extend(contract_addresses)

    return all_contract_addresses

async def process_wallet_addresses(api_keys, wallet_addresses):
    all_results = []
    cache = {}  # Cache to store API responses
    sem = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    async with sem:
        for wallet_address in wallet_addresses:
            api_key = random.choice(api_keys)
            approval_transaction_hashes = await get_approval_transaction_hashes(api_key, wallet_address, cache)
            token_contracts = await get_token_contract_addresses(api_key, approval_transaction_hashes, cache)
            all_results.extend(token_contracts)
    return all_results
async def main():
    results = await process_wallet_addresses(API_KEYS, wallet_addresses)
    contract_counter = Counter(results)
    repeated_contracts = {contract: count for contract, count in contract_counter.items() if count >= 3}
    if repeated_contracts:
        print("Contracts repeated 3 times or more:")
        for contract, count in repeated_contracts.items():
            print(f"Contract Address: {contract}, Count: {count}")
    else:
        print("No contract repeated 3 times or more.")

if __name__ == "__main__":
    asyncio.run(main())
