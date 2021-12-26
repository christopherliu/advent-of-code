using System;
using System.Linq;
					
public class Program
{
	public static void Main()
	{
		string fish = "3,4,3,1,2,1,5,1,1,1,1,4,1,2,1,1,2,1,1,1,3,4,4,4,1,3,2,1,3,4,1,1,3,4,2,5,5,3,3,3,5,1,4,1,2,3,1,1,1,4,1,4,1,5,3,3,1,4,1,5,1,2,2,1,1,5,5,2,5,1,1,1,1,3,1,4,1,1,1,4,1,1,1,5,2,3,5,3,4,1,1,1,1,1,2,2,1,1,1,1,1,1,5,5,1,3,3,1,2,1,3,1,5,1,1,4,1,1,2,4,1,5,1,1,3,3,3,4,2,4,1,1,5,1,1,1,1,4,4,1,1,1,3,1,1,2,1,3,1,1,1,1,5,3,3,2,2,1,4,3,3,2,1,3,3,1,2,5,1,3,5,2,2,1,1,1,1,5,1,2,1,1,3,5,4,2,3,1,1,1,4,1,3,2,1,5,4,5,1,4,5,1,3,3,5,1,2,1,1,3,3,1,5,3,1,1,1,3,2,5,5,1,1,4,2,1,2,1,1,5,5,1,4,1,1,3,1,5,2,5,3,1,5,2,2,1,1,5,1,5,1,2,1,3,1,1,1,2,3,2,1,4,1,1,1,1,5,4,1,4,5,1,4,3,4,1,1,1,1,2,5,4,1,1,3,1,2,1,1,2,1,1,1,2,1,1,1,1,1,4";
		long[] fish_by_age = new long [] {0,0,0,0,0,0,0,0,0};
		for(int i = 0; i < fish.Length; i+=2) {
			fish_by_age[fish[i] - '0']++;
		}
		
		for(int i = 0; i < 256; i++) {
			long new_fish = fish_by_age[0];
			fish_by_age[0] = fish_by_age[1];
			fish_by_age[1] = fish_by_age[2];
			fish_by_age[2] = fish_by_age[3];
			fish_by_age[3] = fish_by_age[4];
			fish_by_age[4] = fish_by_age[5];
			fish_by_age[5] = fish_by_age[6];
			fish_by_age[6] = fish_by_age[7] + new_fish;
			fish_by_age[7] = fish_by_age[8];
			fish_by_age[8] = new_fish;
			
		}
		Console.WriteLine(fish_by_age.Sum());
	}
}