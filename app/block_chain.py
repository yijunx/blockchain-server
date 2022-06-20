import hashlib
from urllib.parse import urlparse
from datetime import datetime, timezone
from typing import List
from app.schema import Transaction, Block
import json


class BlockChain:
    def __init__(self) -> None:
        self.transactions: List[Transaction] = []
        self.chain: List[Block] = []
        self.nodes = set()

        self.new_block(previous_hash="start_hash", proof=100)

    @staticmethod
    def hash(block: Block):

        # This is where we roll up all the data from our block, and hash it.
        block_string = json.dumps(block.dict(), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def is_valid_proof(last_proof: int, proof: int, last_hash: str) -> bool:
        guess = f"{last_proof}{proof}{last_hash}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        # Adjust your mining difficulty here! The more zeroes, the more difficult
        # Be aware that anything above 6 will possibly timeout or crash something
        return guess_hash[:4] == "0000"

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def new_block(self, proof, previous_hash: str) -> Block:

        block = Block(
            index=len(self.chain) + 1,
            timestamp=datetime.now(timezone.utc),
            transactions=self.transactions,
            previous_hash=previous_hash or self.hash(self.chain[-1]),
            proof=proof,
        )

        self.transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, transaction: Transaction) -> int:
        self.transactions.append(transaction)
        return self.last_block.index + 1

    def proof_of_work(self, last_block: Block) -> int:
        last_proof = last_block.proof
        last_hash = self.hash(last_block)

        # here is the mining part
        proof = 0
        while not self.is_valid_proof(last_proof, proof, last_hash):
            proof += 1
        return proof

    def register_node(self, address) -> None:
        
        try:
            parsed_url = urlparse(address)
            self.nodes.add(parsed_url.netloc)
            # nihao:8000
        # if parsed_url.netloc:
        #     self.nodes.add(parsed_url.netloc)
        # elif parsed_url.path:
        #     self.nodes.add(parsed_url.path)
        except:
            raise ValueError('Invalid URL')  

    
    def is_valid_chain(self, chain: List[Block]) -> bool:

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")

            



    

