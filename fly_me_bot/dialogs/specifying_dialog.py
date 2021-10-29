# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Flight booking dialog."""

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import (
                                        TextPrompt,
                                        DateTimePrompt,
                                        ConfirmPrompt,
                                        PromptOptions,
                                        PromptValidatorContext,
)
from botbuilder.core import MessageFactory, BotTelemetryClient, NullTelemetryClient
from sample_21.journey_details import Journey_details

from shared_code.constants.luis_app import LUIS_APPS
from .cancel_and_help_dialog import CancelAndHelpDialog
# from .date_resolver_dialog import DateResolverDialog
from journey_specifier_recognizer import Journey_specifier_recognizer


from helpers.luis_helper import LuisHelper


class Specifying_dialog(CancelAndHelpDialog):
    """Journey specification implementation."""

    def __init__(
        self,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient()
    ):
        """Init the class.

        Args:
            dialog_id (str, optional): Defaults to None.
            telemetry_client (BotTelemetryClient, optional): Insight. Defaults to NullTelemetryClient().
        """
        super(Specifying_dialog, self).__init__(
            dialog_id or Specifying_dialog.__name__, telemetry_client
        )
        self.telemetry_client = telemetry_client

        text_prompt = TextPrompt(TextPrompt.__name__)
        text_prompt.telemetry_client = telemetry_client

        date_time_prompt = DateTimePrompt(
            DateTimePrompt.__name__, Specifying_dialog.datetime_prompt_validator
        )
        date_time_prompt.telemetry_client = telemetry_client

        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__,
            [
                self.destination_step,
                self.origin_step,
                self.departure_date_step,
                self.return_date_step,
                self.budget_step,
                self.confirm_step,
                self.final_step,
            ],
        )
        waterfall_dialog.telemetry_client = telemetry_client

        self.add_dialog(text_prompt)
        self.add_dialog(date_time_prompt)
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        # self.add_dialog(
        #     DateResolverDialog(DateResolverDialog.__name__, self.telemetry_client)
        # )
        self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__

    async def destination_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for destination."""
        journey_details = step_context.options

        if journey_details.destination is None:
            return await step_context.prompt(
                                                TextPrompt.__name__,
                                                PromptOptions(
                    prompt=MessageFactory.text(
                            "To which city would you like to travel?"
                            )
                                                ),
            )  # pylint: disable=line-too-long,bad-continuation
        return await step_context.next(journey_details.destination)

    async def origin_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for origin city."""
        journey_details = step_context.options

        # Check the number of words to guess if it worth asking LUIS
        # to decode the answer.
        if len(step_context.result.split(" ")) > 1:
        # Ask Luis what it thinks about it.
            intent, luis_result = await LuisHelper.execute_luis_query(
                self.luis_recognizer, step_context.context
            )
            result = luis_result.destination
            if result is None:
                return await step_context.prompt(
                            TextPrompt.__name__,
                            PromptOptions(
                                            retry_prompt= MessageFactory.text(
                                                "I do need your destination..."
                                            )
                            )
                )
        else:
            # define intent and luis_result without luis
            intent = LUIS_APPS.INTENTS[LUIS_APPS.INTENT_SPECIFY_JOURNEY_NAME]
            result = step_context.result

        # Capture the response to the previous step's prompt
        journey_details.destination = result
        # Ask for the next
        if journey_details.origin is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("From which city will you be travelling?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(journey_details.origin)

    async def departure_date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Handle waterfall at origin is returned and departure date is checked."""
        # Handle the previous question...
        journey_details = step_context.options

        # Check the number of words to guess if it worth asking LUIS
        # to decode the answer.
        if len(step_context.result.split(" ")) > 1:
        # Ask Luis what it thinks about it.
            intent, luis_result = await LuisHelper.execute_luis_query(
                self.luis_recognizer, step_context.context
            )
            result = luis_result.origin
            if result is None:
                return await step_context.prompt(
                            TextPrompt.__name__,
                            PromptOptions(
                                            prompt= MessageFactory.text(
                                                "Disclose your departure point."
                                            ),
                                            retry_prompt= MessageFactory.text(
                                                "I do need to know your departure point !"
                                            )
                            )
                )
        else:
            # define intent and luis_result without luis
            intent = LUIS_APPS.INTENTS[LUIS_APPS.INTENT_SPECIFY_JOURNEY_NAME]
            result = step_context.result
        # If we are here, we consider that the origin point is legit
        journey_details.origin = result

        # Check if we need to display the request for the date before going
        # down to the next step of the waterfall
        if (
            not journey_details.departure_date
            or
            self.is_ambiguous(journey_details.departure_date)
        ):
            return await step_context.prompt(
                DateTimePrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("When do you want to leave?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation
        return await step_context.next(journey_details.departure_date)

    async def return_date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Handle waterfall at origin is returned and departure date is checked"""
        # Handle the previous question...
        journey_details = step_context.options

        # Check the number of words to guess if it worth asking LUIS to decode
        # the answer.
        if "definite" not in Timex(step_context.result).types:
        # Ask Luis what it thinks about it.
            intent, luis_result = await LuisHelper.execute_luis_query(
                self.luis_recognizer, step_context.context
            )
            result = luis_result.departure_date
            if result is None or self.is_ambiguous(result):
                return await step_context.prompt(
                            DateTimePrompt.__name__,
                            PromptOptions(
                                retry_prompt= MessageFactory.text(
                                    "I do need to know when is your departure!"
                                )
                            )
                )
        else:
            # define intent and luis_result without luis
            intent = LUIS_APPS.INTENTS[LUIS_APPS.INTENT_SPECIFY_JOURNEY_NAME]
            result = Timex(step_context.result)
        # If we are here, we consider that the origin point is legit
        journey_details.departure_date = result

        # Check if we need to display the request for the budget before going
        # down to the next step of the waterfall
        if journey_details.max_budget is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("What is your best budget?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation
        return await step_context.next(journey_details.return_date)

    async def budget_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for the max budget."""
        journey_details = step_context.options

        # Check the number of words to guess if it worth asking LUIS to decode
        # the answer.
        if "definite" not in Timex(step_context.result).types:
        # Ask Luis what it thinks about it.
            intent, luis_result = await LuisHelper.execute_luis_query(
                self.luis_recognizer, step_context.context
            )
            result = luis_result.return_date
            if result is None or self.is_ambiguous(result):
                return await step_context.prompt(
                            DateTimePrompt.__name__,
                            PromptOptions(
                                retry_prompt= MessageFactory.text(
                                    "Do you know when you want to be back!"
                                )
                            )
                )
        else:
            # define intent and luis_result without luis
            intent = LUIS_APPS.INTENTS[LUIS_APPS.INTENT_SPECIFY_JOURNEY_NAME]
            result = Timex(step_context.result)
        # Capture the value.
        journey_details.departure_date = result

        if journey_details.max_budget is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Up to how much are you ready to spend?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation
        return await step_context.next(journey_details.max_budget)


    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Confirm the information the user has provided."""
        journey_details = step_context.options

        # Check the number of words to guess if it worth asking LUIS
        # to decode the answer.
        if len(step_context.result.split(" ")) > 1:
        # Ask Luis what it thinks about it.
            intent, luis_result = await LuisHelper.execute_luis_query(
                self.luis_recognizer, step_context.context
            )
            result = luis_result.max_budget
            if result is None:
                return await step_context.prompt(
                            TextPrompt.__name__,
                            PromptOptions(
                                            retry_prompt= MessageFactory.text(
                                                "Please, give me your top budget!"
                                            )
                            )
                )
        else:
            # define intent and luis_result without luis
            intent = LUIS_APPS.INTENTS[LUIS_APPS.INTENT_SPECIFY_JOURNEY_NAME]
            result = step_context.result
        # If we are here, we consider that the origin point is legit
        journey_details.max_budget = result

        msg = (
            f"Please confirm, I have you traveling to { journey_details.destination }"
            + f" from { journey_details.origin }.\n"
            + f"The departure is on: { journey_details.departure_date} and you return"
            + f" the { journey_details.return_date}.\n"
            + f"Your budget is { journey_details.max_budget} top.\n"
        )

        # Offer a YES/NO prompt.
        return await step_context.prompt(
            ConfirmPrompt.__name__, PromptOptions(prompt=MessageFactory.text(msg))
        )

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Complete the interaction and end the dialog."""
        if step_context.result:
            journey_details = step_context.options
            journey_details.confirm_step = step_context.result

            return await step_context.end_dialog(journey_details)

        return await step_context.end_dialog()



    @staticmethod
    async def datetime_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        """Validate the date provided is in proper form."""
        if prompt_context.recognized.succeeded:
            timex = prompt_context.recognized.value[0].timex.split("T")[0]
            return "definite" in Timex(timex).types

        return False


    def is_ambiguous(self, timex: str) -> bool:
        """Ensure time is correct."""
        timex_property = Timex(timex)
        return "definite" not in timex_property.types
