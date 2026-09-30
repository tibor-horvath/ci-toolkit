// Stand-in for lint / typecheck / test. Extra args (e.g. --shard=1/2) are
// echoed so the run log shows the workflow passed them through.
console.log(`${process.argv[2]} ok`, process.argv.slice(3).join(" "));
