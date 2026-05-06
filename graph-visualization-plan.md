# Plan: Render SPARQL Query as Graph in Notebook

promt: For the Notebook can you add a cell that will render a SPARQL query for the item Q138572994 as a Graph and output it for the Quarto project

Add a new cell to the notebook that:
- Runs a SPARQL query for the item Q138572994 to fetch its relationships as a graph (nodes: items, edges: properties).
- Uses a Python visualization library (e.g., networkx + matplotlib, or pyvis for interactive HTML) to render the graph.
- Outputs the graph in a way compatible with Quarto (static image for PDF/HTML, or interactive HTML for web).

**Steps**
1. Add a new code cell after the SPARQL query cell.
2. In the cell:
   - Use the existing `bindings` or run a new SPARQL query to get item relationships (subject, predicate, object).
   - Parse the results into a graph structure.
   - Use `networkx` to build the graph.
   - Use `matplotlib` (for static) or `pyvis` (for interactive) to render the graph.
   - Display the graph using IPython display functions so Quarto can render it.
3. Ensure the cell works for the current item and is easy to adapt for other items.
4. Add a markdown cell before/after to explain the graph output.

**Relevant files**
- wikidata-item.ipynb — add new code and markdown cells
- wikidata_profile.py — reuse query and parsing functions if possible

**Verification**
1. Run the notebook in Jupyter and Quarto preview to confirm the graph renders.
2. Check that the graph updates if `item_id` changes.
3. Confirm output is visible in the generated HTML in docs/.

**Decisions**
- Use `networkx` + `matplotlib` for static output (widest compatibility with Quarto).
- If interactivity is desired, recommend `pyvis` as an option.

**Further Considerations**
1. If `networkx` or `matplotlib` are not installed, add instructions or a requirements update.
2. For large graphs, consider limiting the number of nodes/edges for clarity.
