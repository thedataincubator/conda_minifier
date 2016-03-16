import subprocess
import sys

import yaml


def get_conda_env_info(fname):
  """Parses environment.yml files for all conda-installed packages."""

  with open(fname) as f:
    environ = yaml.load(f)
    # the pip requirements are a dict so we ignore those
    deps = [l for l in environ['dependencies'] if isinstance(l, basestring)]
    packages = {}
    for dep in deps:
      info = dep.split("=")
      name = info[0]

      if len(info) > 1:
        version = info[1]
      else:
        version = None

      packages[name] = version

    name = environ['name']

  return name, packages


def find_all_deps(packages):
  """Queries conda for the dependencies for the list of packages."""

  dep_list = [find_deps(package, version) for package, version
              in packages.iteritems()]
  return set.union(*dep_list)


def find_deps(package, version):
  """Basically this shells out to `conda info package=version` and
  takes care of the messy parsing logic"""

  pkg_str = "{}={}".format(package, version) if version\
            else package

  query = subprocess.check_output(["conda", "info", pkg_str])

  # remove the lines about fetching package metadata
  info_only = "\n".join(query.split("\n")[2:])

  # two newlines separates each package info area
  deps_versions = [_parse_deps(pkg) for pkg in info_only.split("\n\n")]
  final_deps = set(dep[0] for dep_list in deps_versions
                   for dep in dep_list if dep[0] != '')

  return final_deps


def _parse_deps(pkg_str):
  index = pkg_str.index("dependencies:")
  dep_rows = pkg_str[index:].split("\n")[1:]
  deps_versions = [l.strip().split(" ") for l in dep_rows]
  return deps_versions


def calc_difference(packages, deps):
  source_names = set(packages.keys()) - deps
  return {n: packages[n] for n in source_names}


def output_env(name, source_packages):
  print "name: {}".format(name)
  print "dependencies:"
  for pkg, version in source_packages.iteritems():
    print "- {}={}".format(pkg, version)


def main():
  name, packages = get_conda_env_info(sys.argv[1])
  deps = find_all_deps(packages)
  source_packages = calc_difference(packages, deps)
  output_env(name, source_packages)

if __name__ == "__main__":
  main()
