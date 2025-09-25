import os
import asyncio
from datetime import datetime
import inspect
import logging
import markdown

import dotenv
dotenv.load_dotenv() 

from toolguard.stages_tptd.text_tool_policy_generator import ToolInfo, step1_main
from toolguard.llm.tg_litellm import LitellmModel
from toolguard.logging_utils import add_log_file_handler

logger = logging.getLogger(__name__)


async def gen_all():
    now = datetime.now()
    output_dir = "eval/airline/output"
    out_folder = os.path.join(output_dir, now.strftime("%Y-%m-%d_%H_%M_%S"))
    os.makedirs(out_folder, exist_ok=True)
    add_log_file_handler(os.path.join(out_folder, "run.log"))

    from tau2.domains.airline.tools import AirlineTools
    policy_path = "eval/airline/wiki.md"
    with open(policy_path, 'r', encoding='utf-8') as f:
        policy_text = markdown.markdown(f.read())
    funcs = [member for name, member in inspect.getmembers(AirlineTools, predicate=inspect.isfunction)
        if getattr(member, "__tool__", None)]  # only @is_tool]

    #step1 - tool-policy mapper
    model_name = os.getenv("TOOLGUARD_STEP1_MODEL")
    provider = os.getenv("TOOLGUARD_STEP1_PROVIDER")
    llm = LitellmModel(model_name=model_name, provider=provider)
    tools_info = [ToolInfo.from_function(fn) for fn in funcs]
    step1_out_dir = os.path.join(out_folder, "step1")
    await step1_main(policy_text, tools_info, step1_out_dir, llm, short=True)


    #step2 - tool_guard code generation
    #step1_out_dir = "eval/airline/output/2025-09-25_17_45_43/step1"
    from toolguard.core import generate_guards_from_tool_policies
    return await generate_guards_from_tool_policies(funcs,
        from_step1_path=step1_out_dir,
        to_step2_path=out_folder,
        tool_names=["cancel_reservation"],  # ["book_reservation", "update_reservation_passengers", "update_reservation_baggages", "update_reservation_flights"],
        app_name="airline"
    )


if __name__ == '__main__':
    from toolguard.logging_utils import init_logging
    init_logging()
    asyncio.run(gen_all())
    logger.info("done")
