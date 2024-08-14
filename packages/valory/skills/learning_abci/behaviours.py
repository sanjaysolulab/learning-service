# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2024 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains round behaviours of LearningAbciApp."""

from abc import ABC
import dataclasses
from typing import Generator, Set, Type, cast

from packages.valory.skills.abstract_round_abci.base import AbstractRound
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)
from packages.valory.skills.learning_abci.models import Params, SharedState
from packages.valory.skills.learning_abci.payloads import (
    APICheckPayload,
    DecisionMakingPayload,
    TxPreparationPayload,
)
from packages.valory.skills.learning_abci.rounds import (
    APICheckRound,
    DecisionMakingRound,
    Event,
    LearningAbciApp,
    SynchronizedData,
    TxPreparationRound,
)
####################################changes#########
# from packages.valory.contracts.gnosis_safe.contract import (
#     GnosisSafeContract,
#     SafeOperation,
# )
# from packages.valory.contracts.multisend.contract import MultiSendContract
from packages.valory.protocols.contract_api import ContractApiMessage
####################################changes#########

HTTP_OK = 200
GNOSIS_CHAIN_ID = "gnosis"
TX_DATA = b"0x"
SAFE_GAS = 0
VALUE_KEY = "value"
TO_ADDRESS_KEY = "to_address"


# SAFE_GAS = 0
# CID_PREFIX = "f01701220"
# WXDAI = "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d"
# BET_AMOUNT_FIELD = "bet_amount"
# SUPPORTED_STRATEGY_LOG_LEVELS = ("info", "warning", "error")
# ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
# NEW_LINE = "\n"
# QUOTE = '"'
# TWO_QUOTES = '""'
# INIT_LIQUIDITY_INFO = LiquidityInfo()


class LearningBaseBehaviour(BaseBehaviour, ABC):  # pylint: disable=too-many-ancestors
    """Base behaviour for the learning_abci skill."""

    @property
    def synchronized_data(self) -> SynchronizedData:
        """Return the synchronized data."""
        return cast(SynchronizedData, super().synchronized_data)

    @property
    def params(self) -> Params:
        """Return the params."""
        return cast(Params, super().params)

    @property
    def local_state(self) -> SharedState:
        """Return the state."""
        return cast(SharedState, self.context.state)

    # @property
    # def txs_value(self) -> int:
    #     """Get the total value of the transactions."""
    #     return sum(batch.value for batch in self.multisend_batches)

    # @property
    # def multi_send_txs(self) -> List[dict]:
    #     """Get the multisend transactions as a list of dictionaries."""
    #     return [dataclasses.asdict(batch) for batch in self.multisend_batches]

    # @property
    # def safe_tx_hash(self) -> str:
    #     """Get the safe_tx_hash."""
    #     return self._safe_tx_hash

    # @safe_tx_hash.setter
    # def safe_tx_hash(self, safe_hash: str) -> None:
    #     """Set the safe_tx_hash."""
    #     length = len(safe_hash)
    #     if length != TX_HASH_LENGTH:
    #         raise ValueError(
    #             f"Incorrect length {length} != {TX_HASH_LENGTH} detected "
    #             f"when trying to assign a safe transaction hash: {safe_hash}"
    #         )
    #     self._safe_tx_hash = safe_hash[2:]

class APICheckBehaviour(LearningBaseBehaviour):  # pylint: disable=too-many-ancestors
    """APICheckBehaviour"""

    matching_round: Type[AbstractRound] = APICheckRound

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            price = yield from self.get_price()
            payload = APICheckPayload(sender=sender, price=price)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()

    def get_price(self):
        """Get token price from Coingecko"""
        # result = yield from self.get_http_response("coingecko.com")
        yield
        price = 1.0
        self.context.logger.info(f"Price is {price}")
        return price


class DecisionMakingBehaviour(
    LearningBaseBehaviour
):  # pylint: disable=too-many-ancestors
    """DecisionMakingBehaviour"""

    matching_round: Type[AbstractRound] = DecisionMakingRound

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            event = self.get_event()
            payload = DecisionMakingPayload(sender=sender, event=event)

####################################changes#########
        # with self.context.benchmark_tool.measure(self.behaviour_id).local():
        #     sender = self.context.agent_address
        #     event = self.get_event2()
        #     payload = DecisionMakingPayload(sender=sender, event=event)
####################################changes#########

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()

    def get_event(self):
        """Get the next event"""
        # Using the token price from the previous round, decide whether we should make a transfer or not
        event = Event.DONE.value
        self.context.logger.info(f"Event is {event}")
        return event


    def get_event2(self):
        """Get the next event"""
        # Using the token price from the previous round, decide whether we should make a transfer or not
        event = Event.DONE.value
        self.context.logger.info(f"Event is {self.synchronized_data.safe_contract_address}")
        return event
        
        # response_msg = yield from self.get_contract_api_response(
        #     performative=ContractApiMessage.Performative.GET_STATE,
        #     contract_address=self.synchronized_data.safe_contract_address,
        #     contract_id=str(GnosisSafeContract.contract_id),
        #     contract_callable="get_raw_safe_transaction_hash",
        # )

####################################changes########

#     def _build_multisend_safe_tx_hash(self) -> WaitableConditionType:
#         """Prepares and returns the safe tx hash for a multisend tx."""
#         response_msg = yield from self.get_contract_api_response(
#             performative=ContractApiMessage.Performative.GET_STATE,  # type: ignore
#             contract_address=self.synchronized_data.safe_contract_address,
#             contract_id=str(GnosisSafeContract.contract_id),
#             contract_callable="get_raw_safe_transaction_hash",
#             to_address=self.params.multisend_address,
#             value=self.txs_value,
#             data=self.multisend_data,
#             safe_tx_gas=SAFE_GAS,
#             operation=SafeOperation.DELEGATE_CALL.value,
#         )

#         if response_msg.performative != ContractApiMessage.Performative.STATE:
#             self.context.logger.error(
#                 "Couldn't get safe tx hash. Expected response performative "  # type: ignore
#                 f"{ContractApiMessage.Performative.STATE.value}, "  # type: ignore
#                 f"received {response_msg.performative.value}: {response_msg}."
#             )
#             return False

#         tx_hash = response_msg.state.body.get("tx_hash", None)
#         if tx_hash is None or len(tx_hash) != TX_HASH_LENGTH:
#             self.context.logger.error(
#                 "Something went wrong while trying to get the buy transaction's hash. "
#                 f"Invalid hash {tx_hash!r} was returned."
#             )
#             return False

#         # strip "0x" from the response hash
#         self.safe_tx_hash = tx_hash
#         return True
# ####################################changes#########

class TxPreparationBehaviour(
    LearningBaseBehaviour
):  # pylint: disable=too-many-ancestors
    """TxPreparationBehaviour"""

    matching_round: Type[AbstractRound] = TxPreparationRound

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            tx_hash = yield from self.get_tx_hash()
            payload = TxPreparationPayload(
                sender=sender, tx_submitter=None, tx_hash=tx_hash
            )

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()

    def get_tx_hash(self):
        """Get the tx hash"""
        # We need to prepare a 1 wei transfer from the safe to another (configurable) account.
        yield
        tx_hash = None
        self.context.logger.info(f"Transaction hash is {tx_hash}")
        return tx_hash


class LearningRoundBehaviour(AbstractRoundBehaviour):
    """LearningRoundBehaviour"""

    initial_behaviour_cls = APICheckBehaviour
    abci_app_cls = LearningAbciApp  # type: ignore
    behaviours: Set[Type[BaseBehaviour]] = [  # type: ignore
        APICheckBehaviour,
        DecisionMakingBehaviour,
        TxPreparationBehaviour,
    ]
