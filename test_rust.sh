#!/usr/bin/env bash

repo_name=$(basename "$(git rev-parse --show-toplevel)")
PROJECT_NAME=${PROJECT_NAME:=$repo_name}
PROJECT_TYPE=${PROJECT_TYPE:-python}

linters=(clippy)
lint_project(){
  case $1 in
    # https://flake8.pycqa.org/en/latest/, https://www.pylint.org/
    clippy )
      cargo clippy
      ;;
    * )
      printf '\nUsage: %s LINTER\nAvailable LINTERs: %s' \
        "${FUNCNAME[0]}" "${linters[*]}"
      return 1
      ;;
  esac
}

testers=(cargo_run)
test_project(){
  case $1 in
    cargo_run )
      cargo run
      ;;
    * )
      printf '\nUsage: %s TESTER\nAvailable TESTER: %s' \
        "${FUNCNAME[0]}" "${testers[*]}"
      return 1
      ;;
  esac
}

echo 'Installing dependencies ...'
cargo build
echo
for linter in "${linters[@]}"; do
  printf '%-50s' "Linting $PROJECT_TYPE with $linter ... "
  if lint=$(lint_project "$linter" 2>&1); then
    echo 'PASSED ✅'
  else
    echo 'FAILED ❌'
    echo "$lint"
    echo
    exit 1
  fi
done
for tester in "${testers[@]}"; do
  printf '%-50s' "Testing $PROJECT_TYPE with $tester ... "
  if test=$(test_project "$tester" 2>&1); then
    echo 'PASSED ✅'
  else
    echo 'FAILED ❌'
    echo "$test"
    echo
    exit 1
  fi
  echo Done.
  echo
done
