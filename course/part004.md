# Part 4
## Exploring real workloads, and additional tools

Today we'll explore our running workloads, services, ingresses, and other Kubernetes resources we have mentioned but not delved into.

## Additional tools

In previous parts of this course we have used the `kubectl` tool for all our interactions with Kubernetes. Once you have a solid understanding of `kubectl` and the YAML that drives resources, it's a good time to explore other tools you are likely to encounter. Neither of these tools can perform every operation that `kubectl` can, but they still well suited to certain roles and tasks. For example, someone who is mostly interested in seeing when a failure is occurring or looking at logs could do so very quickly with either tool below.

### Additional tools with substantial user bases

- [Lens](https://k8slens.dev/)
- [K9s](https://k9scli.io/)

### Caution!

Skipping `kubectl` in favor of GUI-based tools, or trying to avoid understanding YAML is a recipe for disaster. Certain operations are only able to be performed in `kubectl`, and the official documentation assumes you have a solid understanding of YAML.

## Guided exploration of Kubernetes using Datadog

Follow along to learn how to use Datadog dashboards to quickly see the status of your Kubernetes resources.