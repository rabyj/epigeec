#!/usr/bin/env python
"""Additional unit tests for filter subcommand edge cases"""
# pylint: disable=import-outside-toplevel, wrong-import-position, import-error
import os
import shutil
import sys
import tempfile
import unittest

import h5py
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import python.core.config as config

sys.path.append(config.CORE_DIR)
import python.core.main as epimain


class FilterEdgeCaseTest(unittest.TestCase):
    """Test edge cases for the filter subcommand, particularly around bin boundaries."""

    def setUp(self):
        """Set up temporary directory and file paths."""
        self.test_dir = tempfile.mkdtemp()
        self.chrom_sizes_path = os.path.join(self.test_dir, "test.chrom.sizes")
        self.bed_path = os.path.join(self.test_dir, "test.bed")
        self.bigwig_path = os.path.join(self.test_dir, "test.bw")
        self.hdf5_input = os.path.join(self.test_dir, "input.hdf5")
        self.hdf5_output = os.path.join(self.test_dir, "output.hdf5")

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def create_chrom_sizes(self, sizes_dict):
        """Create a chromosome sizes file.

        Args:
            sizes_dict: Dictionary of chromosome name -> size
        """
        with open(self.chrom_sizes_path, "w", encoding="utf8") as f:
            for chrom, size in sizes_dict.items():
                f.write(f"{chrom}\t{size}\n")

    def create_bed_file(self, regions):
        """Create a BED file with specified regions.

        Args:
            regions: List of tuples (chrom, start, end)
        """
        with open(self.bed_path, "w", encoding="utf8") as f:
            for chrom, start, end in regions:
                f.write(f"{chrom}\t{start}\t{end}\n")

    def create_bigwig(self, chrom_data, chrom_sizes):
        """Create a bigWig file with signal data.

        Args:
            chrom_data: Dictionary of chromosome -> list of (start, end, value) tuples
            chrom_sizes: Dictionary of chromosome -> size
        """
        try:
            import pyBigWig
        except ImportError:
            # Try to use an existing test file instead
            test_signals = os.path.join(config.TEST_DIR, "files", "signal")
            if os.path.exists(test_signals):
                # Use first available signal file as fallback
                for fname in os.listdir(test_signals):
                    src = os.path.join(test_signals, fname)

                    shutil.copy(src, self.bigwig_path)
                    return
            self.skipTest("pyBigWig not installed and no test signals available")

        bw = pyBigWig.open(self.bigwig_path, "w")
        header = [(chrom, size) for chrom, size in chrom_sizes.items()]
        bw.addHeader(header)

        for chrom, intervals in chrom_data.items():
            chroms = [chrom] * len(intervals)
            starts = [x[0] for x in intervals]
            ends = [x[1] for x in intervals]
            values = [x[2] for x in intervals]
            bw.addEntries(chroms, starts, ends=ends, values=values)

        bw.close()

    def count_filtered_bins(self, hdf5_path):
        """Count total number of bins (non-NaN values) in filtered HDF5.

        Args:
            hdf5_path: Path to HDF5 file

        Returns:
            Dictionary of chromosome -> count of non-NaN bins
        """
        counts = {}
        with h5py.File(hdf5_path, "r") as f:
            # Get the signal group (should be only one group at root level)
            signal_id = os.path.basename(hdf5_path)
            if signal_id in f:
                group = f[signal_id]
                for chrom_name, chrom_arr in group.items():
                    data = chrom_arr[:]
                    counts[chrom_name] = np.sum(~np.isnan(data))
            else:
                # Fallback: try to find the first group
                for group in f.values():
                    if isinstance(group, h5py.Group):
                        for chrom_name, chrom_arr in group.items():
                            data = chrom_arr[:]
                            counts[chrom_name] = np.sum(~np.isnan(data))
                        break
        return counts

    def get_bin_values(self, hdf5_path, chrom):
        """Get non-NaN bin values from HDF5 file.

        Args:
            hdf5_path: Path to HDF5 file
            chrom: Chromosome name

        Returns:
            Array of non-NaN values
        """
        with h5py.File(hdf5_path, "r") as f:
            signal_id = os.path.basename(hdf5_path)
            if signal_id in f:
                group = f[signal_id]
            else:
                for group in f.values():
                    if isinstance(group, h5py.Group):
                        break

            data = group[chrom][:]
            return data[~np.isnan(data)]

    def test_exact_bin_boundaries(self):
        """Test filtering with BED regions that exactly match bin boundaries."""
        resolution = 10000
        chrom_size = 100000  # Exactly 10 bins

        self.create_chrom_sizes({"chr1": chrom_size})

        # Create bigWig with uniform signal across entire chromosome
        # This will create 10 bins of value 1.0
        self.create_bigwig({"chr1": [(0, chrom_size, 1.0)]}, {"chr1": chrom_size})

        # Convert to HDF5
        args = [
            "to_hdf5",
            "-bw",
            self.bigwig_path,
            self.chrom_sizes_path,
            str(resolution),
            self.hdf5_input,
        ]
        epimain.main(args)

        # BED file with regions that exactly match bins 2, 3, 4
        # [20000, 30000), [30000, 40000), [40000, 50000)
        self.create_bed_file(
            [
                ("chr1", 20000, 30000),
                ("chr1", 30000, 40000),
                ("chr1", 40000, 50000),
            ]
        )

        # Run filter
        args = [
            "filter",
            "--select",
            self.bed_path,
            self.hdf5_input,
            self.chrom_sizes_path,
            self.hdf5_output,
        ]
        epimain.main(args)

        # Check that exactly 3 bins are kept
        counts = self.count_filtered_bins(self.hdf5_output)
        self.assertEqual(
            counts["chr1"],
            3,
            "Should keep exactly 3 bins for regions matching 3 exact bins",
        )

    def test_last_bin_of_chromosome(self):
        """Test that the last bin of a chromosome is handled correctly."""
        resolution = 10000
        chrom_size = 95000  # 9.5 bins, so 10 bins total (0-9)

        self.create_chrom_sizes({"chr1": chrom_size})

        # Create bigWig with signal covering entire chromosome
        # This ensures all bins including the last one have data
        self.create_bigwig({"chr1": [(0, chrom_size, 1.0)]}, {"chr1": chrom_size})

        args = [
            "to_hdf5",
            "-bw",
            self.bigwig_path,
            self.chrom_sizes_path,
            str(resolution),
            self.hdf5_input,
        ]
        epimain.main(args)

        # Select only the last bin [90000, 95000)
        self.create_bed_file([("chr1", 90000, 95000)])

        args = [
            "filter",
            "--select",
            self.bed_path,
            self.hdf5_input,
            self.chrom_sizes_path,
            self.hdf5_output,
        ]
        epimain.main(args)

        counts = self.count_filtered_bins(self.hdf5_output)
        self.assertEqual(
            counts.get("chr1", 0),
            1,
            "Should keep exactly 1 bin for last chromosome bin",
        )

    def test_region_spanning_bin_boundary(self):
        """Test region that spans exactly from one bin boundary to another."""
        resolution = 10000
        chrom_size = 100000

        self.create_chrom_sizes({"chr1": chrom_size})

        # Create bigWig with uniform signal
        self.create_bigwig({"chr1": [(0, chrom_size, 1.0)]}, {"chr1": chrom_size})

        args = [
            "to_hdf5",
            "-bw",
            self.bigwig_path,
            self.chrom_sizes_path,
            str(resolution),
            self.hdf5_input,
        ]
        epimain.main(args)

        # Region from 20000 to 50000 should cover bins 2, 3, 4 (NOT 5)
        self.create_bed_file([("chr1", 20000, 50000)])

        args = [
            "filter",
            "--select",
            self.bed_path,
            self.hdf5_input,
            self.chrom_sizes_path,
            self.hdf5_output,
        ]
        epimain.main(args)

        counts = self.count_filtered_bins(self.hdf5_output)
        self.assertEqual(
            counts["chr1"],
            3,
            "Region [20000, 50000) should cover exactly 3 bins (2, 3, 4)",
        )

    def test_single_base_at_bin_boundary(self):
        """Test that a single base at a bin boundary is handled correctly."""
        resolution = 10000
        chrom_size = 100000

        self.create_chrom_sizes({"chr1": chrom_size})

        # Create bigWig with uniform signal across entire chromosome
        self.create_bigwig({"chr1": [(0, chrom_size, 1.0)]}, {"chr1": chrom_size})

        args = [
            "to_hdf5",
            "-bw",
            self.bigwig_path,
            self.chrom_sizes_path,
            str(resolution),
            self.hdf5_input,
        ]
        epimain.main(args)

        # Single base at position 30000 (start of bin 3)
        # [30000, 30001) should only touch bin 3
        self.create_bed_file([("chr1", 30000, 30001)])

        args = [
            "filter",
            "--select",
            self.bed_path,
            self.hdf5_input,
            self.chrom_sizes_path,
            self.hdf5_output,
        ]
        epimain.main(args)

        counts = self.count_filtered_bins(self.hdf5_output)
        self.assertEqual(
            counts["chr1"], 1, "Single base at bin boundary should touch exactly 1 bin"
        )

    def test_off_by_one_regression(self):
        """Regression test: ensure we don't include the bin at end position."""
        resolution = 1000
        chrom_size = 10000  # 10 bins

        self.create_chrom_sizes({"chr1": chrom_size})

        # Create bigWig with uniform signal
        self.create_bigwig({"chr1": [(0, chrom_size, 1.0)]}, {"chr1": chrom_size})

        args = [
            "to_hdf5",
            "-bw",
            self.bigwig_path,
            self.chrom_sizes_path,
            str(resolution),
            self.hdf5_input,
        ]
        epimain.main(args)

        # Old bug: [0, 5000) with i <= end_bin would include bins 0,1,2,3,4,5 (6 bins)
        # Correct: [0, 5000) with i < end_bin should include bins 0,1,2,3,4 (5 bins)
        self.create_bed_file([("chr1", 0, 5000)])

        args = [
            "filter",
            "--select",
            self.bed_path,
            self.hdf5_input,
            self.chrom_sizes_path,
            self.hdf5_output,
        ]
        epimain.main(args)

        counts = self.count_filtered_bins(self.hdf5_output)
        self.assertEqual(
            counts["chr1"],
            5,
            "Half-open interval [0, 5000) should include exactly 5 bins, not 6",
        )

    def test_multiple_chromosomes_last_bins(self):
        """Test filtering with multiple chromosomes, focusing on last bins."""
        resolution = 10000

        chrom_sizes = {
            "chr1": 95000,  # 10 bins
            "chr2": 105000,  # 11 bins
            "chr3": 100000,  # 10 bins
        }
        self.create_chrom_sizes(chrom_sizes)

        # Create bigWig with signal across all chromosomes
        bigwig_data = {chrom: [(0, size, 1.0)] for chrom, size in chrom_sizes.items()}
        self.create_bigwig(bigwig_data, chrom_sizes)

        args = [
            "to_hdf5",
            "-bw",
            self.bigwig_path,
            self.chrom_sizes_path,
            str(resolution),
            self.hdf5_input,
        ]
        epimain.main(args)

        # Select last bin of each chromosome
        self.create_bed_file(
            [
                ("chr1", 90000, 95000),  # Last bin of chr1
                ("chr2", 100000, 105000),  # Last bin of chr2
                ("chr3", 90000, 100000),  # Last bin of chr3
            ]
        )

        args = [
            "filter",
            "--select",
            self.bed_path,
            self.hdf5_input,
            self.chrom_sizes_path,
            self.hdf5_output,
        ]
        epimain.main(args)

        counts = self.count_filtered_bins(self.hdf5_output)
        self.assertEqual(counts.get("chr1", 0), 1, "chr1 should have 1 bin")
        self.assertEqual(counts.get("chr2", 0), 1, "chr2 should have 1 bin")
        self.assertEqual(counts.get("chr3", 0), 1, "chr3 should have 1 bin")


if __name__ == "__main__":
    unittest.main()
