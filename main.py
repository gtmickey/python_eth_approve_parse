from web3 import Web3, AsyncWeb3
import asyncio

abi = '[{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"}]';


async def main():
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider('https://mainnet.infura.io/v3/xxxx'))

    # 1. 检索某个区块中的合约授权的数据， 合约授权 调用的 方法为 approve.
    # approve 方法的 topic id，固定值
    approve_topic = '0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925'
    # 查询数据的区块范围，以及topic事件
    filter_params = {
        'fromBlock': hex(19859649),
        'toBlock': hex(19859650),
        'topics': [approve_topic],  # 可为[], 如果为空数组，则查询所有的topics
    }
    f = await w3.eth.filter(filter_params)
    # 获取 区块中的 logs
    logs = await w3.eth.get_filter_logs(f.filter_id)
    for log in logs:

        hex_amount = log['data'].hex()
        if hex_amount == '0x':
            hex_amount = '0x0'
        contract = log['topics'][0].hex()  # 在approve_topic 中  topics[0] 为 合约地址
        owner = log['topics'][1].hex()  # 在approve_topic 中  topics[1] 为 owner，即钱包用户地址
        spender = log['topics'][2].hex()  # 在approve_topic 中  topics[2] 为 spender，即被授权人，合约或者个人地址
        tx_hash = log['transactionHash'].hex()
        block_number = log['blockNumber']
        log_index = log['logIndex']

        print("contract", contract)  # 合约地址
        print("owner", owner)  # 授权人
        print("spender", spender)  # 被授权合约
        print("amount 16", hex_amount)  # 授权数量16进制
        print("amount 十进制", int(hex_amount, 16))  # 授权数量10进制
        print("tx_hash", tx_hash)  # 此次授权的交易hash
        print("block_number", block_number)  # 此次授权的交易的block number
        print("log_index", log_index)  # 此次授权的交易的 log_index，整型值， 一次交易中，可能会存在多次 approve, 以log_index大的为新的数据
        print("---------------------------------------")

    # 2. 通过以下方法可以查询某个特定合约（如USDT） 被授权了多少的数量
    usdt_contract = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
    owner = '0x81d3D78FEFb33562D807686c0A0e589E5979EacD'
    spender = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
    contract = w3.eth.contract(address=Web3.to_checksum_address(usdt_contract.lower()), abi=abi)
    allowance = await  contract.functions.allowance(Web3.to_checksum_address(owner.lower()),
                                                    Web3.to_checksum_address(spender.lower())).call()
    print('allowance', allowance)


if __name__ == "__main__":
    asyncio.run(main())
