import asyncio
import logging
import json
from os.path import join
from typing import Callable, List, Optional

import mellea
import sys
from openai import AzureOpenAI
# Replace the OpenAI class in sys.modules so anything importing sees AzureOpenAI
sys.modules['openai'].OpenAI = AzureOpenAI
from mellea.backends.openai import OpenAIBackend



from toolguard.gen_py.consts import *
from toolguard.gen_py.domain_from_funcs import generate_domain_from_functions
from toolguard.data_types import RuntimeDomain, ToolPolicy, FileTwin
from toolguard.gen_py.domain_from_openapi import generate_domain_from_openapi
from toolguard.runtime import ToolGuardsCodeGenerationResult
from toolguard.gen_py.tool_guard_generator import ToolGuardGenerator
import toolguard.utils.pytest as pytest
import toolguard.utils.venv as venv
import toolguard.utils.pyright as pyright
from toolguard.common.py import unwrap_fn

logger = logging.getLogger(__name__)

async def generate_toolguards_from_functions(app_name: str, tool_policies: List[ToolPolicy], py_root:str, funcs: List[Callable], module_roots: Optional[List[str]]=None)->ToolGuardsCodeGenerationResult:
    assert funcs, "Funcs cannot be empty"
    logger.debug(f"Starting... will save into {py_root}")

    if not module_roots:
        if len(funcs)>0:
            module_roots = list({unwrap_fn(func).__module__.split(".")[0] for func in funcs})
    assert module_roots

    #Domain from functions
    domain = generate_domain_from_functions(py_root, app_name, funcs, module_roots)
    return await generate_toolguards_from_domain(app_name, tool_policies, py_root, domain)

async def generate_toolguards_from_openapi(app_name: str, tool_policies: List[ToolPolicy], py_root:str, openapi_file:str)->ToolGuardsCodeGenerationResult:
    logger.debug(f"Starting... will save into {py_root}")

    #Domain from OpenAPI
    domain = generate_domain_from_openapi(py_root, app_name, openapi_file)
    return await generate_toolguards_from_domain(app_name, tool_policies, py_root, domain)

async def generate_toolguards_from_domain(app_name: str, tool_policies: List[ToolPolicy], py_root:str, domain: RuntimeDomain)->ToolGuardsCodeGenerationResult:

    #Setup env
    venv.run(join(py_root, PY_ENV), PY_PACKAGES)
    pyright.config(py_root)
    pytest.configure(py_root)

    #tools
    tools_w_poilicies = [tool_policy for tool_policy in tool_policies if len(tool_policy.policy_items) > 0]


    # start of wrapping code for mellea

    # model_options = {"extra_query": {"api-version": "2024-08-01-preview"}}
    #
    # backend = OpenAIBackend(
    #         model_id="gpt-5-chat-2025-08-07",
    #         #formatter=TemplateFormatter(model_id="ibm-granite/granite-3.2-8b-instruct"),
    #         #base_url="https://eteopenai.azure-api.net",
    #         #base_url="https://eteopenai.azure-api.net/openai/deployments/gpt-5-chat-2025-08-07/chat/completions?api-version=2024-08-01-preview",
    #         #base_url="https://eteopenai.azure-api.net/openai/deployments/gpt-5-chat-2025-08-07",
    #         #api_key="c7765b7a6c9048feab6433fc6b05e32e",
    #         #model_options=model_options,
    #     )
    #
    # from mellea import MelleaSession
    # session = MelleaSession(backend=backend)
    # with session:

    tool_results = await asyncio.gather(*[
        ToolGuardGenerator(app_name, tool_policy, py_root, domain, PY_ENV)\
            .generate()
        for tool_policy in tools_w_poilicies
    ])

    # end of the wrapper


    tools_result = {tool.tool_name: res
        for tool, res
        in zip(tools_w_poilicies, tool_results)
    }
    return ToolGuardsCodeGenerationResult(
        domain=domain,
        tools=tools_result
    ).save(py_root)
