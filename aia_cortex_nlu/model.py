from dataclasses import dataclass
from typing import Dict
from datetime import datetime, timezone
from typing import List, Dict

@dataclass
class AIABreadcrumb:
	name: str
	creationDate: datetime

@dataclass
class AIASemanticGraphNode:
	originalText: str
	tag: str
	index: int
	relationType: str
	parent: Dict
	semanticNodeTree: str

@dataclass
class AIACmd:
	origin: str
	typeCmd: str
	cmd: str
	parameters: List
