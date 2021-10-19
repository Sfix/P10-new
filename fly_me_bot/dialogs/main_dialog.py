# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import (
    MessageFactory,
    TurnContext,
    BotTelemetryClient,
    NullTelemetryClient,
)
from botbuilder.schema import InputHints

from journey_details import Journey_details
from journey_specifier_recognizer import Journey_specifier_recognizer
from helpers.luis_helper import LuisHelper

from .specifying_dialog import Specifying_dialog

from shared_code.constants.luis_app import LUIS_APPS


class MainDialog(ComponentDialog):
    def __init__(
        self,
        luis_recognizer: Journey_specifier_recognizer,
        specifying_dialog: Specifying_dialog,
        telemetry_client: BotTelemetryClient = None,
    ):
        super(MainDialog, self).__init__(MainDialog.__name__)
        self.telemetry_client = telemetry_client or NullTelemetryClient()

        text_prompt = TextPrompt(TextPrompt.__name__)
        text_prompt.telemetry_client = self.telemetry_client

        specifying_dialog.telemetry_client = self.telemetry_client

        wf_dialog = WaterfallDialog(
            "WFDialog", [self.intro_step, self.act_step, self.final_step]
        )
        wf_dialog.telemetry_client = self.telemetry_client

        self._luis_recognizer = luis_recognizer
        self._specifying_dialog_id = specifying_dialog.id

        self.add_dialog(text_prompt)
        self.add_dialog(specifying_dialog)
        self.add_dialog(wf_dialog)

        self.initial_dialog_id = "WFDialog"

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "NOTE: LUIS is not configured. To enable all capabilities, add 'LuisAppId', 'LuisAPIKey' and "
                    "'LuisAPIHostName' to the appsettings.json file.",
                    input_hint=InputHints.ignoring_input,
                )
            )

            return await step_context.next(None)
        message_text = (
            str(step_context.options)
            if step_context.options
            else "Hello, I'm please to help you. Where do you want to go?"
        )
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Act accordingly to the intent found.

        Args:
            step_context (WaterfallStepContext): Waterfall of the Bot.

        Returns:
            DialogTurnResult: Next step according to the context.
        """
        if not self._luis_recognizer.is_configured:
            # LUIS is not configured, we just run the BookingDialog path with an empty Journey_detailsInstance.
            return await step_context.begin_dialog(
                self._specifying_dialog_id, Journey_details()
            )

        # Call LUIS and gather any potential journey details. (Note the TurnContext has the response to the prompt.)
        intent, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )

        if intent == LUIS_APPS.INTENTS[LUIS_APPS.INTENT_SPECIFY_JOURNEY_NAME] and luis_result:
            # Show a warning for Origin and Destination if we can't resolve them.
            await MainDialog._show_warning_for_unsupported_cities(
                step_context.context, luis_result
            )

            # Run the Journey Specify giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._specifying_dialog_id, luis_result)

        if intent == LUIS_APPS.INTENTS[LUIS_APPS.INTENT_GREETINGS_NAME]:
            greeting_text = "Hello to you too. Can I know where you want to go?"
            prompt_message = MessageFactory.text(
                greeting_text, greeting_text, InputHints.expecting_input
            )
            await step_context.context.send_activity(greeting_text)

        if intent == LUIS_APPS.INTENTS[LUIS_APPS.INTENT_HELP_NAME]:
            help_text = "How can I help you."
            get_help_message = MessageFactory.text(
                help_text, help_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(get_help_message)
        else:
            didnt_understand_text = (
                "Sorry, I didn't get that. Please try asking in a different way"
            )
            didnt_understand_message = MessageFactory.text(
                didnt_understand_text, didnt_understand_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(didnt_understand_message)

        return await step_context.next(None)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Handle the final message.

        Args:
            step_context (WaterfallStepContext): Waterfall of the bot.

        Returns:
            DialogTurnResult: Next turn of the dialog.
        """
        # If the child dialog ("BookingDialog") was cancelled or the user failed to confirm,
        # the Result here will be null.
        if step_context.result is not None:
            result = step_context.result

            # Now we have all the booking details call the booking service.

            # If the call to the booking service was successful tell the user.
            # time_property = Timex(result.travel_date)
            # travel_date_msg = time_property.to_natural_language(datetime.now())
            msg_txt  = f"I have understood you want to "
            msg_txt += f"go to {result.destination} from {result.origin}"
            msg_txt += f" on {result.travel_date}"
            msg_txt += f" and your best budget is {result.max_budget}."
            message = MessageFactory.text(msg_txt, msg_txt, InputHints.ignoring_input)
            await step_context.context.send_activity(message)

        prompt_message = "What else can I do for you?"
        return await step_context.replace_dialog(self.id, prompt_message)

    @staticmethod
    async def _show_warning_for_unsupported_cities(
        context: TurnContext, luis_result: Journey_details
    ) -> None:
        """
        Show a warning if the requested From or To cities are recognized as entities but they are not in the Airport entity list.

        In some cases LUIS will recognize the From and To composite entities as a valid cities but the From and To Airport values
        will be empty if those entity values can't be mapped to a canonical item in the Airport.
        """
        if luis_result.unsupported_airports:
            message_text = (
                f"Sorry but the following airports are not supported:"
                f" {', '.join(luis_result.unsupported_airports)}"
            )
            message = MessageFactory.text(
                message_text, message_text, InputHints.ignoring_input
            )
            await context.send_activity(message)
