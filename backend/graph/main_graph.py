from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from backend.db.persistence import initialize_database
from backend.graph.nodes.application_answers import application_answers_node
from backend.graph.nodes.apply_helper import apply_helper_node
from backend.graph.nodes.cover_letter import cover_letter_node
from backend.graph.nodes.gap_detector import gap_detector_node
from backend.graph.nodes.jd_analyzer import jd_analyzer_node
from backend.graph.nodes.optimizer import optimizer_node
from backend.graph.nodes.planner import planner_node
from backend.graph.nodes.resume_analyzer import resume_analyzer_node
from backend.graph.state import JobAgentState


initialize_database()

checkpointer = MemorySaver()

graph = StateGraph(JobAgentState)

graph.add_node("planner", planner_node)
graph.add_node("jd_analyzer", jd_analyzer_node)
graph.add_node("resume_analyzer", resume_analyzer_node)
graph.add_node("gap_detector", gap_detector_node)
graph.add_node("optimizer", optimizer_node)
graph.add_node("cover_letter", cover_letter_node)
graph.add_node("application_answers", application_answers_node)
graph.add_node("apply_helper", apply_helper_node)

graph.add_edge(START, "planner")
graph.add_edge("planner", "jd_analyzer")
graph.add_edge("jd_analyzer", "resume_analyzer")
graph.add_edge("resume_analyzer", "gap_detector")
graph.add_edge("gap_detector", "optimizer")
graph.add_edge("optimizer", "cover_letter")
graph.add_edge("cover_letter", "application_answers")
graph.add_edge("application_answers", "apply_helper")
graph.add_edge("apply_helper", END)

job_agent = graph.compile(checkpointer=checkpointer)
