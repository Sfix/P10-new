# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Flight booking dialog."""

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, BotTelemetryClient, NullTelemetryClient
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
        self._luis_recognizer = None

        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__,
            [
                self.destination_step,
                self.origin_step,
                self.travel_date_step,
                self.budget_step,
                self.confirm_step,
                self.final_step,
            ],
        )
        waterfall_dialog.telemetry_client = telemetry_client

        self.add_dialog(text_prompt)
        # self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        # self.add_dialog(
        #     DateResolverDialog(DateResolverDialog.__name__, self.telemetry_client)
        # )
        # self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__

    async def destination_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for destination."""
        journey_details = step_context.options

        if journey_details.destination is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("To what city would you like to travel?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation
# TODO : Serge Ajouter le renseignement du reste

        return await step_context.next(journey_details.destination)

    async def origin_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for origin city."""
        journey_details = step_context.options

        # Ask Luis what it thinks about it.
        intent, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )

        # Capture the response to the previous step's prompt
        journey_details.destination = step_context.result
        if journey_details.origin is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("From what city will you be travelling?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(journey_details.origin)

    async def travel_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for travel date.
        This will use the DATE_RESOLVER_DIALOG."""

        journey_details = step_context.options

        # Capture the results of the previous step
        journey_details.origin = step_context.result
        if not journey_details.travel_date or self.is_ambiguous(
            journey_details.travel_date
        ):
            return await step_context.reprompt_dialog()

        return await step_context.next(journey_details.travel_date)

    async def budget_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for the max budget."""
        journey_details = step_context.options

        # Capture the response to the previous step's prompt
        journey_details.travel_date = step_context.result
        if journey_details.origin is None:
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

        # Capture the results of the previous step
        journey_details.max_budget = step_context.result
        msg = (
            f"Please confirm, I have you traveling to: { journey_details.destination }"
            f" from: { journey_details.origin } on: { journey_details.travel_date}."
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

    def is_ambiguous(self, timex: str) -> bool:
        """Ensure time is correct."""
        timex_property = Timex(timex)
        return "definite" not in timex_property.types
