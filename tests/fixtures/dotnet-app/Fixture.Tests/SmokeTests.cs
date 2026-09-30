// The namespace carries the shard token: the workflow filters each shard by
// `FullyQualifiedName~.unit.`, so a test must live under `.unit.` to run.
namespace Fixture.Tests.unit;

public class SmokeTests
{
    [Fact]
    public void Passes() => Assert.True(true);
}
