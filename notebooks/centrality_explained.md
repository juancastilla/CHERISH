*What characterises an important factor?* 

**Centrality** measures are a vital tool for understanding networks, often also known as graphs.These algorithms use graph theory to calculate the importance of any given node in a network. They cut through noisy data, revealing parts of the network that need attention – but they all work differently. Each measure has its own definition of *importance*, so you need to understand how they work to find the best one for your graph visualization applications. Let’s look at some social network analysis measures, how they work, and when to use them.'

### Degree centrality (local importance)

> - **Definition:** Degree centrality assigns an importance score based simply on the number of links held by each node.

> - **What it tells us:** How many direct, ‘one hop’ connections each node has to other nodes in the network.

> - **When to use it:** For finding very connected individuals, popular individuals, individuals who are likely to hold most information or individuals who can quickly connect with the wider network.

> - **A bit more detail:** Degree centrality is the simplest measure of node connectivity. Sometimes it’s useful to look at *in-degree* (number of inbound links) and *out-degree* (number of outbound links) as distinct measures, for example when looking at transactional data or account activity.